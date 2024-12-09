# 等待根分区扫描

需要阻塞等待并发标记线程扫描完根分区。

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::wait_for_root_region_scanning() {
    Ticks start = Ticks::now();
    // 需要阻塞等待并发标记线程扫描完根分区
    // 因为在GC期间会移动对象
    // 所以需要在GC之前确保所有对象都已经被正确扫描
    bool waited = concurrent_mark()->wait_until_root_region_scan_finished();
    Tickspan wait_time;
    if (waited) {
        // 记录等了多久
        wait_time = (Ticks::now() - start);
    }
    phase_times()->record_root_region_scan_wait_time(wait_time.seconds() * MILLIUNITS);
}
```
