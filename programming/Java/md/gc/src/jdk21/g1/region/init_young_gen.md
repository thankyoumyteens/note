# 初始化新生代 region

在堆空间初始化时(G1CollectedHeap::initialize 方法), 会调用 recalculate_min_max_young_length() 函数计算出新生代的预期范围, 为后面设置新生代大小做准备。另外, 在这里 G1 也会设置要保留的 region 数量。

保留的 region: 通过-XX:G1ReservePercent 设置, 默认值是堆空间的 10%。这个值是为了保留一些堆空间以避免发生 to-space overflow/exhausted。

to-space exhausted: 在 Young GC 的 Evacuation 阶段, G1 会把 eden region 中的存活对象都移动到新申请的 survivor region 中, 原来的 survivor region 中的存活对象会根据阈值移动到新申请的 survivor region 中或者晋升到老年代 region 中, 如果此时堆空间不够, 可能会导致 Full GC 耗费大量时间。

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

// 调用栈:
// G1CollectedHeap::expand g1CollectedHeap.cpp:1112
// G1CollectedHeap::initialize g1CollectedHeap.cpp:1477
// Universe::initialize_heap universe.cpp:843
// universe_init universe.cpp:785
// init_globals init.cpp:124
// Threads::create_vm threads.cpp:549
// JNI_CreateJavaVM_inner jni.cpp:3577
// JNI_CreateJavaVM jni.cpp:3668
// InitializeJVM java.c:1506
// JavaMain java.c:415
// ThreadJavaMain java_md.c:650
// start_thread 0x00007ffff7c94ac3
// clone3 0x00007ffff7d26850
void G1Policy::record_new_heap_size(uint new_number_of_regions) {
  // 初始化要保留的region数
  // _reserve_factor = G1ReservePercent / 100.0, 默认10%
  double reserve_regions_d = (double) new_number_of_regions * _reserve_factor;
  _reserve_regions = (uint) ceil(reserve_regions_d);
  // 计算新生代的预期范围
  _young_gen_sizer.heap_size_changed(new_number_of_regions);
  // 更新堆空间占用的字节数: _target_occupancy
  _ihop_control->update_target_occupancy(new_number_of_regions * HeapRegion::GrainBytes);
}

/////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1YoungGenSizer.cpp //
/////////////////////////////////////////////////

/**
 * 计算新生代的预期范围
 */
void G1YoungGenSizer::heap_size_changed(uint new_number_of_heap_regions) {
  recalculate_min_max_young_length(new_number_of_heap_regions, &_min_desired_young_length,
          &_max_desired_young_length);
}
```

计算完新生代的预期范围之后, 会在 G1Policy::init 中设置新生代的 region 数量:

```cpp
//////////////////////////////////////////
// src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////

// 调用栈:
// G1Policy::init g1Policy.cpp
// G1CollectedHeap::initialize g1CollectedHeap.cpp:1483
// Universe::initialize_heap universe.cpp:843
// universe_init universe.cpp:785
// init_globals init.cpp:124
// Threads::create_vm threads.cpp:549
// JNI_CreateJavaVM_inner jni.cpp:3577
// JNI_CreateJavaVM jni.cpp:3668
// InitializeJVM java.c:1506
// JavaMain java.c:415
// ThreadJavaMain java_md.c:650
// start_thread 0x00007ffff7c94ac3
// clone3 0x00007ffff7d26850
void G1Policy::init(G1CollectedHeap* g1h, G1CollectionSet* collection_set) {
  _g1h = g1h;
  _collection_set = collection_set;

  assert(Heap_lock->owned_by_self(), "Locking discipline.");
  // 调整MaxNewSize的值
  // 传入整个堆空间的region数量
  _young_gen_sizer.adjust_max_new_size(_g1h->max_regions());
  // 记录当前空闲region的数量
  _free_regions_at_end_of_collection = _g1h->num_free_regions();

  // 设置新生代region数量
  update_young_length_bounds();

  // 初始化cset
  _collection_set->start_incremental_building();
}

/////////////////////////////////////////////////
// src/hotspot/share/gc/g1/g1YoungGenSizer.cpp //
/////////////////////////////////////////////////

/**
 * 调整MaxNewSize的值
 */
void G1YoungGenSizer::adjust_max_new_size(uint number_of_heap_regions) {

  uint temp = _min_desired_young_length;
  uint result = _max_desired_young_length;
  // 计算新生代region的范围
  recalculate_min_max_young_length(number_of_heap_regions, &temp, &result);
  // 计算新生代region最大字节数
  // HeapRegion::GrainBytes是每个region的大小
  size_t max_young_size = result * HeapRegion::GrainBytes;
  if (max_young_size != MaxNewSize) {
    // 更新MaxNewSize的值
    FLAG_SET_ERGO(MaxNewSize, max_young_size);
  }
}
```
