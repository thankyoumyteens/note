# 处理 SATB 队列

SATB队列的长度为1k，由参数G1SATBBufferSize控制，表示每个队列有1000个对象。

每个队列有一个参数G1SATBBufferEnqueueingThresholdPercent（默认值是60），表示当一个队列满了之后，首先进行过滤处理，过滤后如果使用率超过这个阈值则新分配一个队列，否则重用这个队列。过滤的条件就是这个对象属于新分配对象（位于next和top之间），且还没有标记，后续会处理该对象。

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
  // 因为并发标记线程和Java线程并发运行，所以SATB会不断地变化，
  // 与DCQ类似，satb队列也会在装满后放入satb队列集合中，
  // 这里只对放入集合中的SATB队列做处理
  // 因为标记老年代可能要花费的时间比较多，所以增加了标记检查，
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
    // satb队列集合是全局的，需要加锁访问
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
    // 集合空了，返回false，跳出循环
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
  // 把对象标记到_nextMarkBitMap位图中(染成灰色)并计数，
  // 根扫描子阶段中也用到了这个方法
  if (_cm->par_mark_and_count(obj, hr, _marked_bytes_array, _card_bm)) {

    HeapWord* global_finger = _cm->finger();

    if (is_below_finger(obj, global_finger)) {
      if (obj->is_typeArray()) {
        // 对象是一个数组，无须继续追踪。直接记录数组的长度
        process_grey_object<false>(obj);
      } else {
        // 把对象push到本地队列，等待后续处理
        push(obj);
      }
    }
  }
}

inline void CMTask::push(oop obj) {
  HeapWord* objAddr = (HeapWord*) obj;
  assert(_g1h->is_in_g1_reserved(objAddr), "invariant");
  assert(!_g1h->is_on_master_free_list(
              _g1h->heap_region_containing((HeapWord*) objAddr)), "invariant");
  assert(!_g1h->is_obj_ill(obj), "invariant");
  assert(_nextMarkBitMap->isMarked(objAddr), "invariant");

  if (_cm->verbose_high()) {
    gclog_or_tty->print_cr("[%u] pushing " PTR_FORMAT, _worker_id, p2i((void*) obj));
  }

  if (!_task_queue->push(obj)) {
    // The local task queue looks full. We need to push some entries
    // to the global stack.

    if (_cm->verbose_medium()) {
      gclog_or_tty->print_cr("[%u] task queue overflow, "
                             "moving entries to the global stack",
                             _worker_id);
    }
    move_entries_to_global_stack();

    // this should succeed since, even if we overflow the global
    // stack, we should have definitely removed some entries from the
    // local queue. So, there must be space on it.
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
