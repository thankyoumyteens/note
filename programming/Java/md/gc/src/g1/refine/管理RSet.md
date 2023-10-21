# 管理RSet

JVM在每次给引用类型的字段赋值时，会通过写屏障把引用者对象在全局卡表中所在的card插入到dirty card queue(DCQ)中。DCQ分为两种：

1. 每个用户线程都有一个自己的DCQ，DCQ的大小由参数-XX:G1UpdateBufferSize设置，默认值是256，表示最多可以存放256个引用关系
2. JVM有一个全局的DCQ，所有用户线程共享这个DCQ

JVM中有一个全局的dirty card queue set(DCQS)用于存放已经满了的DCQ。当DCQ已放满256个引用关系时，用户线程会把这个DCQ添加到DCQS中。如果在添加时发现DCQS已经满了，那么说明引用变更太多了，Refine线程已经处理不过来了，用户线程就不会继续往DCQS里添加了，并且这个用户线程会暂停其他代码执行，替代Refine线程来更新RSet。

把对象加入到DCQ的代码：

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\ptrQueue.hpp

```cpp
class PtrQueue VALUE_OBJ_CLASS_SPEC {
public:
  /**
   * ptr：指向引用者的对象所在的card
   */
  void enqueue(void* ptr) {
    // _active表示是否需要记录引用关系的变化
    if (!_active) {
      return;
    } else {
      // 判断当前DCQ还有没有空间
      // 如果有，则直接加入
      // 如果满了，则看一下DCQS是否还有空间，
      // 来决定是把当前DCQ添加到DCQS中，并分配一个新的DCQ，
      // 还是暂停其他代码执行，替代Refine线程来更新RSet
      enqueue_known_active(ptr);
    }
  }
}
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\ptrQueue.cpp

```cpp
void PtrQueue::enqueue_known_active(void* ptr) {
  // _index变量用于记录对象最后一次入队的位置，初始值为_sz(表示缓冲区为空)，
  // 随着对象的入队操作，其值会逐渐减小到0
  // _sz变量表示DCQ能记录多少个对象
  // _buf是DCQ
  while (_index == 0) {
    // _index为0，表示DCQ已经满了，
    // 需要把当前DCQ加入到DCQS，并申请新的DCQ
    handle_zero_index();
  }
  // 对象加入DCQ，其值会逐渐减小
  _index -= oopSize;
  // index的步长是一个对象的大小，需要换算成数组的索引
  // return _index / oopSize;
  _buf[byte_index_to_index((int)_index)] = ptr;
}

/**
 * 处理DCQ满了的情况
 */
void PtrQueue::handle_zero_index() {
  if (_buf != NULL) {
    if (!should_enqueue_buffer()) {
      return;
    }

    if (_lock) {
      // 进入这里，说明使用的是全局的DCQ
      void** buf = _buf;
      _buf = NULL;
      // 把全局DCQ放入到DCQS中
      locking_enqueue_completed_buffer(buf);
      // 如果_buf不为null，说明其他的线程已经成功地为全局DCQ申请到空间了，直接返回
      if (_buf != NULL) {
        return;
      }
    } else {
      // 把用户线程的DCQ放入到DCQS中
      // qset()方法返回DCQS
      if (qset()->process_or_enqueue_complete_buffer(_buf)) {
        // 返回值为真，说明用户线程暂停执行应用代码，帮助处理DCQ，
        // 把这个DCQ清空，重用DCQ
        _sz = qset()->buffer_size();
        _index = _sz;
        return;
      }
    }
  }
  // 执行到这里，说明DCQS没满，并且原来的DCQ已经加入到DCQS了，
  // 申请一个新的DCQ
  _buf = qset()->allocate_buffer();
  _sz = qset()->buffer_size();
  _index = _sz;
}

/**
 * 把全局DCQ放入到DCQS中
 */
void PtrQueue::locking_enqueue_completed_buffer(void** buf) {
  // 检查当前线程是否拥有锁
  assert(_lock->owned_by_self(), "Required.");

  // 在将全局DCQ加入DCQS之前，会先解锁
  // 因为在enqueue_complete_buffer函数内部可能会获取到相同的锁，
  // 为了避免死锁，需要先解锁
  _lock->unlock();
  // 将DCQ加入DCQS
  qset()->enqueue_complete_buffer(buf);
  // 将DCQ加入DCQS后立即重新锁定
  _lock->lock_without_safepoint_check();
}

/**
 * 把用户线程的DCQ放入到DCQS中
 */
bool PtrQueueSet::process_or_enqueue_complete_buffer(void** buf) {
  // 检查是否需要用户线程帮忙更新RSet
  if (Thread::current()->is_Java_thread()) {
    // 需要
    if (_max_completed_queue == 0 || _max_completed_queue > 0 &&
        _n_completed_buffers >= _max_completed_queue + _completed_queue_padding) {
      // 用户线程处理DCQ
      bool b = mut_process_buffer(buf);
      if (b) {
        // 返回值为true，表示用户线程暂停执行应用代码，帮助处理DCQ，
        return true;
      }
    }
  }
  // 把用户线程的DCQ放入到DCQS中
  enqueue_complete_buffer(buf);
  return false;
}

/**
 * 把DCQ放入到DCQS中
 */
void PtrQueueSet::enqueue_complete_buffer(void** buf, size_t index) {
  MutexLockerEx x(_cbl_mon, Mutex::_no_safepoint_check_flag);
  // DCQS是一个链表，BufferNode是它的节点
  BufferNode* cbn = BufferNode::new_from_buffer(buf);
  cbn->set_index(index);
  // 链表为空
  if (_completed_buffers_tail == NULL) {
    // _completed_buffers_head：链表的头节点
    // _completed_buffers_tail：链表的尾节点
    _completed_buffers_head = cbn;
    _completed_buffers_tail = cbn;
  } else {
    // 新节点追加到链表末尾
    _completed_buffers_tail->set_next(cbn);
    _completed_buffers_tail = cbn;
  }
  _n_completed_buffers++;
  // 判断是否需要有Refine线程工作
  if (!_process_completed && _process_completed_threshold >= 0 &&
      _n_completed_buffers >= _process_completed_threshold) {
    _process_completed = true;
    // 如果没有线程工作通过notify通知启动
    if (_notify_when_complete) {
      // 通知0号Refine线程
      _cbl_mon->notify();
    }
  }
}
```
