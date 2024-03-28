# 处理 SATB 队列

SATB队列的长度为1k, 由参数G1SATBBufferSize控制, 表示每个队列有1000个对象。

每个队列有一个参数G1SATBBufferEnqueueingThresholdPercent(默认值是60), 表示当一个队列满了之后, 首先进行过滤处理, 过滤后如果使用率超过这个阈值则新分配一个队列, 否则重用这个队列。过滤的条件就是这个对象属于新分配对象(位于next和top之间), 且还没有标记, 后续会处理该对象。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.cpp

```cpp
void CMTask::drain_satb_buffers() {
  if (has_aborted()) {
    return;
  }

  // 设置标记表示正在处理satb队列
  _draining_satb_buffers = true;
  // 用来处理satb队列
  CMSATBBufferClosure satb_cl(this, _g1h);
  // satb队列集合
  SATBMarkQueueSet& satb_mq_set = JavaThread::satb_mark_queue_set();
  // 因为并发标记线程和Java线程并发运行, 所以SATB会不断地变化, 
  // 与DCQ类似, satb队列也会在装满后放入satb队列集合中, 
  // 这里只对放入集合中的SATB队列做处理
  // 因为标记老年代可能要花费的时间比较多, 所以增加了标记检查, 
  // 如果发现有溢出、终止、线程同步等满足终止条件的情况都会设置停止标志来终止标记动作
  while (!has_aborted() &&
         satb_mq_set.apply_closure_to_completed_buffer(&satb_cl)) {
    statsOnly( ++_satb_buffers_processed );
    regular_clock_call();
  }

  _draining_satb_buffers = false;

  decrease_limits();
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\satbQueue.cpp

```cpp
bool SATBMarkQueueSet::apply_closure_to_completed_buffer(SATBBufferClosure* cl) {
  BufferNode* nd = NULL;
  {
    // satb队列集合是全局的, 需要加锁访问
    MutexLockerEx x(_cbl_mon, Mutex::_no_safepoint_check_flag);
    // 从集合中取出位于头节点的satb队列
    if (_completed_buffers_head != NULL) {
      nd = _completed_buffers_head;
      // 头节点指向下一个节点
      _completed_buffers_head = nd->next();
      if (_completed_buffers_head == NULL) {
        _completed_buffers_tail = NULL;
      }
      _n_completed_buffers--;
      if (_n_completed_buffers == 0) {
        _process_completed = false;
      }
    }
  }
  if (nd != NULL) {
    void **buf = BufferNode::make_buffer_from_node(nd);
    assert(_sz % sizeof(void*) == 0, "invariant");
    size_t limit = ObjPtrQueue::byte_index_to_index((int)_sz);
    for (size_t i = 0; i < limit; ++i) {
      if (buf[i] != NULL) {
        // 处理satb队列
        cl->do_buffer(buf + i, limit - i);
        break;
      }
    }
    // 释放内存
    deallocate_buffer(buf);
    return true;
  } else {
    // 集合空了, 返回false, 跳出循环
    return false;
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.cpp

```cpp
class CMSATBBufferClosure : public SATBBufferClosure {
private:
  CMTask* _task;
  G1CollectedHeap* _g1h;

  void do_entry(void* entry) const {
    _task->increment_refs_reached();
    HeapRegion* hr = _g1h->heap_region_containing_raw(entry);
    if (entry < hr->next_top_at_mark_start()) {
      oop obj = static_cast<oop>(entry);
      // 标记satb中记录的对象
      _task->make_reference_grey(obj, hr);
    }
  }
public:
  virtual void do_buffer(void** buffer, size_t size) {
    for (size_t i = 0; i < size; ++i) {
      do_entry(buffer[i]);
    }
  }
};
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.inline.hpp

```cpp
inline void CMTask::make_reference_grey(oop obj, HeapRegion* hr) {
  // 把对象标记到_nextMarkBitMap位图中(染成灰色)并计数
  if (_cm->par_mark_and_count(obj, hr, _marked_bytes_array, _card_bm)) {

    HeapWord* global_finger = _cm->finger();

    if (is_below_finger(obj, global_finger)) {
      if (obj->is_typeArray()) {
        // 对象是一个数组, 无须继续追踪。直接记录数组的长度
        // false表示不继续扫描对象的字段
        process_grey_object<false>(obj);
      } else {
        // 把对象push到本地队列, 等待后续处理它的字段
        push(obj);
      }
    }
  }
}

inline bool ConcurrentMark::par_mark_and_count(oop obj,
                                               HeapRegion* hr,
                                               size_t* marked_bytes_array,
                                               BitMap* task_card_bm) {
  HeapWord* addr = (HeapWord*)obj;
  // 通过CAS修改nextMarkBitMap的值
  if (_nextMarkBitMap->parMark(addr)) {
    count_object(obj, hr, marked_bytes_array, task_card_bm);
    return true;
  }
  return false;
}

inline void CMTask::push(oop obj) {
  HeapWord* objAddr = (HeapWord*) obj;
  // 添加到本地队列
  if (!_task_queue->push(obj)) {
    // 本地队列满了, 把本地队列中的一部分对象移动到全局标记栈中
    move_entries_to_global_stack();

    // 重新尝试把这个对象添加到本地队列
    bool success = _task_queue->push(obj);
    assert(success, "invariant");
  }

  statsOnly( int tmp_size = _task_queue->size();
             if (tmp_size > _local_max_size) {
               _local_max_size = tmp_size;
             }
             ++_local_pushes );
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.cpp

```cpp
void CMTask::move_entries_to_global_stack() {
  // global_stack_transfer_size
  // 用于控制要从本地队列转移多少个对象到全局标记栈中
  // 默认是16
  oop buffer[global_stack_transfer_size];

  int n = 0;
  oop obj;
  // 先把本地队列中的对象移动到缓冲区中
  while (n < global_stack_transfer_size && _task_queue->pop_local(obj)) {
    buffer[n] = obj;
    ++n;
  }

  if (n > 0) {
    statsOnly( ++_global_transfers_to; _local_pops += n );
    // 把缓冲区中的对象入栈
    if (!_cm->mark_stack_push(buffer, n)) {
      // 栈溢出了, 设置终止标记
      set_has_aborted();
    } else {
      // 转移成功
      statsOnly( int tmp_size = _cm->mark_stack_size();
                 if (tmp_size > _global_max_size) {
                   _global_max_size = tmp_size;
                 }
                 _global_pushes += n );
    }
  }

  // 把本地队列中的对象移动到全局标记栈的行为非常耗费资源, 
  // 调用这个方法让处理队列的操作更频繁, 
  // 避免再出现本地队列满了的情况
  decrease_limits();
}
```
