# 向RSet中添加引用关系

JVM在每次给引用类型的字段赋值时，会插入一个写后屏障(post-write barrier)，post-write barrier中会做下面的处理：

1. 在global card table中找到该字段所在的card，并设置为dirty_card
2. 如果当前是应用线程，每个Java线程有一个dirty card queue(DCQ)，把该card插入队列
3. G1有一个全局卡表(global card table)，它的每个card都对应某个Region中的512字节的内存空间，如果一个card变脏(dirty)，就说明对应的region存在跨region的引用

赋值动作到此结束，接下来RSet的更新操作交由多个ConcurrentG1RefineThread并发完成，Refine线程会取出若干个DCQ，遍历每个DCQ中记录的card，并进行处理：

1. 根据card的地址，计算出card所在的Region
2. 如果Region不存在，或者Region在新生代中，或者该Region在回收集中，则不进行处理
3. 使用G1UpdateRSOrPushRefOopClosure::do_oop_nv()函数处理该card

do_oop_nv()函数中处理该card的代码：

```cpp
// to是被引用对象所在的Region
to->rem_set()->add_reference(p, _worker_i);
```

add_reference()函数的处理：

1. 首先会使用稀疏PRT记录引用关系，当引用逐渐增多，RSet占用的内存空间越来越大，就会将这种引用关系记录的详细程度往下降，描述不再那么详细进而存储更多的引用关系。当稀疏表中的某一个entry中的cards数组长度为4之后，就会将该entry中的所有记录转到细粒度PRT中。当细粒度PRT的记录数达到了G1设定的阈值之后，会转为使用粗粒度。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionRemSet.cpp

```cpp
// 向RSet中添加引用关系
void OtherRegionsTable::add_reference(OopOrNarrowOopStar from, int tid) {
  uint cur_hrm_ind = hr()->hrm_index();
  // 计算引用者所在的card
  int from_card = (int)(uintptr_t(from) >> CardTableModRefBS::card_shift);
  // 为了提高效率，有一个卡表的缓存，在缓存中发现引用已经处理则返回
  if (FromCardCache::contains_or_replace((uint)tid, cur_hrm_ind, from_card)) {
    return;
  }

  // 大对象可能跨region，因此需要找到该对象的头部region
  HeapRegion* from_hr = _g1h->heap_region_containing_raw(from);
  // 获取region对应的region_index
  RegionIdx_t from_hrm_ind = (RegionIdx_t) from_hr->hrm_index();

  // 如果RSet已经变成粗粒度位图
  // 也就是说RSet里面记录的是引用者对象所在的Region
  // 而不是对象对应的卡表地址，那么可以直接返回
  if (_coarse_map.at(from_hrm_ind)) {
    return;
  }

  // RSet还没有变成粗粒度位图，就要找一个细粒度PRT记录引用
  size_t ind = from_hrm_ind & _mod_max_fine_entries_mask;
  PerRegionTable* prt = find_region_table(ind, from_hr);
  if (prt == NULL) {
    // 加锁，避免多个线程同时访问一个Region对应的RSet
    MutexLockerEx x(_m, Mutex::_no_safepoint_check_flag);
    // 再次确认有没有细粒度PRT、针对并发情况
    prt = find_region_table(ind, from_hr);
    if (prt == NULL) {
      // 计算card index
      uintptr_t from_hr_bot_card_index =
        uintptr_t(from_hr->bottom())
          >> CardTableModRefBS::card_shift;
      CardIdx_t card_index = from_card - from_hr_bot_card_index;
      // 先看看能不能存储到稀疏PRT中
      if (G1HRRSUseSparseTable && _sparse_table.add_card(from_hrm_ind, card_index)) {
        return;
      }
      // 稀疏PRT满了，继续执行
      if (_n_fine_entries == _max_fine_entries) {
        // 细粒度PRT已经满了，调用delete_region_table()函数
        // 把细粒度PRT数组中最大的一个细粒度PRT元素迁移到粗粒度位图中，
        // 并返回该元素
        prt = delete_region_table();
        // 重新初始化该元素，即清空内容
        prt->init(from_hr, false);
      } else {
        // 细粒度PRT没满，分配一个新的细粒度PRT来存储
        prt = PerRegionTable::alloc(from_hr);
        link_to_all(prt);
      }

      // 此时稀疏PRT已经满了，并且已经申请了一个细粒度PRT
	    // 那么就要将稀疏PRT中的信息添迁移到细粒度PRT中
      PerRegionTable* first_prt = _fine_grain_regions[ind];
      prt->set_collision_list_next(first_prt);
      _fine_grain_regions[ind] = prt;
      _n_fine_entries++;
      if (G1HRRSUseSparseTable) {
        // 把稀疏PRT里面的数据迁移到细粒度PRT中
        SparsePRTEntry *sprt_entry = _sparse_table.get_entry(from_hrm_ind);
        for (int i = 0; i < SparsePRTEntry::cards_num(); i++) {
          CardIdx_t c = sprt_entry->card(i);
          if (c != SparsePRTEntry::NullEntry) {
            prt->add_card(c);
          }
        }
        // 迁移成功后删除稀疏PRT
        bool res = _sparse_table.delete_entry(from_hrm_ind);
      }
    }
  }
  // 存储到细粒度PRT
  prt->add_reference(from);
}
```
