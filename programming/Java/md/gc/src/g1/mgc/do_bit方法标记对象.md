# do_bit 方法标记对象

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.cpp

```cpp
class CMBitMapClosure : public BitMapClosure {
private:
  CMBitMap*                   _nextMarkBitMap;
  ConcurrentMark*             _cm;
  CMTask*                     _task;

public:
  bool do_bit(size_t offset) {
    // 找到对象的起始地址
    HeapWord* addr = _nextMarkBitMap->offsetToHeapWord(offset);
    assert(_nextMarkBitMap->isMarked(addr), "invariant");
    assert( addr < _cm->finger(), "invariant");

    statsOnly( _task->increase_objs_found_on_bitmap() );
    assert(addr >= _task->finger(), "invariant");

    // 更新局部_finger
    _task->move_finger_to(addr);
    // 标记这个对象的字段指向的对象，
    // 它会把字段指向的对象添加到本地队列中
    // 处理本地队列中也用到了这个方法
    _task->scan_object(oop(addr));
    // 处理一部分本地队列
    _task->drain_local_queue(true);
    // 处理一部分全局标记栈
    _task->drain_global_stack(true);

    return !_task->has_aborted();
  }
};
```
