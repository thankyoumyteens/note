# Young GC

```cpp
// --- src/hotspot/share/gc/g1/g1CollectedHeap.cpp --- //

void G1CollectedHeap::do_collection_pause_at_safepoint_helper() {
    ResourceMark rm;

    IsGCActiveMark active_gc_mark;
    GCIdMark gc_id_mark;
    SvcGCMarker sgcm(SvcGCMarker::MINOR);

    GCTraceCPUTime tcpu(_gc_tracer_stw);

    _bytes_used_during_gc = 0;

    // 是否把本次STW作为并发标记的初始标记阶段
    policy()->decide_on_concurrent_start_pause();
    // in_concurrent_start_gc() 返回 _in_concurrent_start_gc 的值(bool值)
    // _in_concurrent_start_gc 的值会在前面的 decide_on_concurrent_start_pause() 中决定
    // 把它保存到变量中, 因为稍后启动并发标记线程(G1ConcurrentMarkThread)后,
    // _in_concurrent_start_gc 的值可能会在别的地方修改
    bool should_start_concurrent_mark_operation = collector_state()->in_concurrent_start_gc();

    // 执行GC
    G1YoungCollector collector(gc_cause());
    collector.collect();

    // 此时可以开启并发标记线程了,
    // 因为过早开启并发标记线程会导致并发标记的日志和STW期间的日志混到一起
    if (should_start_concurrent_mark_operation) {
        verifier()->verify_bitmap_clear(true /* above_tams_only */);
        // 注意: start_concurrent_cycle() 函数执行后, 并发标记线程可能就会开始并发地运行了
        // 确保在这之后执行的任何操作, 都不会假设只有GC线程在运行
        // 但是实际上并发标记工作直到调用SuspendibleThreadSet::desynchronize()函数退出安全点后才会开始
        start_concurrent_cycle(collector.concurrent_operation_is_full_mark());
        // 把_is_idle设置为false
        // _is_idle为true时表示垃圾回收器处于空闲状态
        ConcurrentGCBreakpoints::notify_idle_to_active();
    }
}
```
