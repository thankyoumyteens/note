# RSet

为解决对象跨代引用所带来的问题，G1用记忆集(RSet)记录从非收集部分指向收集部分的指针的集合。

通常有两种方法记录引用关系：Point Out 和 Point in，G1使用了Point In的方法。

- Point out：比如objA.field = objB，Point out会在objA的RSet中记录objB的地址
- Point in：比如objA.field = objB，Point in会在objB的RSet中记录objA的地址，Point in相当于一种反向引用

在G1中提供了3种收集算法：Yong GC、Mixed GC和Full GC。Yong GC总是收集所有新生代Region，Mixed GC会收集所有的新生代Region以及部分老年代Region，而Full GC则是对所有的Region处理。

Region之间有5种引用关系：

1. Region内部有引用关系，无论是新生代Region还是老年代Region内部的引用，都无需记录引用关系，因为回收的时候是针对一个Region而言，即这个Region要么被回收要么不回收，回收的时候会遍历整个Region，所以无需记录这种额外的引用关系
2. 新生代Region到新生代Region之间有引用关系，这个无需记录，原因在于G1的3中回收算法都会全量处理新生代Region，所以它们都会被遍历，所以无需记录新生代到新生代之间的引用
3. 新生代Region到老年代Region之间有引用关系，这个无需记录，Yong GC针对的是所有新生代Region，无需这个引用关系，Mixed GC也会回收所有新生代Region，那么遍历新生代Region的时候自然能找到引用的老年代Region，所以也无需这个引用，对于Full GC来说更无需这个引用关系，所有的Region都会被处理
4. 老年代Region到新生代Region之间有引用关系，这个需要记录，在Yong GC的时候有两种GC Root，一个就是栈和方法区中变量的引用，另外一个就是老年代Region到新生代Region的引用
5. 老年代Region到老年代Region之间有引用关系，这个需要记录，在Mixed GC的时候可能只有部分老年代Region被回收，所以必须记录引用关系，快速找到哪些对象是活跃的

在线程运行过程中，如果对象的引用发生了变化（通常就是赋值操作），就必须要通知RSet，更改其中的记录，但对于一个Region来说，里面的对象有可能被很多Region所引用，这就要求这个Region记录所有引用者的信息。为此G1使用了卡表PRT（Per region Table）来记录这种变化。

每个Region都包含了一个PRT，它通过HeapRegion里面的HeapRegionRemSet获得，而HeapRegionRemSet包含了一个OtherRegionsTable，也就是PRT。

OtherRegionsTable使用了三种不同的粒度来描述引用，一个对象可能被引用的次数不固定，引用的次数可能很多也可能很少，为了提高效率，才用了动态化的数据结构存储。主要有以下三种粒度：

1. 稀疏PRT：通过哈希表方式来存储。默认长度为4
2. 细粒度PRT：PRT指针的数组
3. 粗粒度：通过位图来表示，位图中的每一位代表一个Region

每个PRT元素使用的是HeapRegion的起始地址加上一个位图，这个位图描述这一个Region的引用情况，每一位对应Region的512字节，所以它的大小为HeapRegionSize%512，这样可以使用更少的内存存储更多的引用关系。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegion.hpp

```cpp
// Region
class HeapRegion: public G1OffsetTableContigSpace {
  friend class VMStructs;
 private:

  HeapRegionRemSet* _rem_set;
  // ...
};
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionRemSet.hpp

```cpp
// RSet
class HeapRegionRemSet : public CHeapObj<mtGC> {
// ...
private:
  // ...
  OtherRegionsTable _other_regions;
  // ...
}

// PRT
class OtherRegionsTable VALUE_OBJ_CLASS_SPEC {
  // ...
  // 粗粒度
  BitMap      _coarse_map;
  // ...
  // 细粒度PRT
  PerRegionTable** _fine_grain_regions;
  // ...
  // 稀疏PRT
  SparsePRT   _sparse_table;
  // ...
};
```

首先会使用稀疏PRT记录引用，当引用逐渐增多，RSet占用的内存空间越来越大，就会将这种引用关系记录的详细程度往下降，描述不再那么详细进而存储更多的引用关系。当稀疏表中的某一个entry中的cards数组长度为4之后，就会将该entry中的所有记录转到细粒度PRT中。当细粒度PRT的记录数达到了G1设定的阈值之后，会转为使用粗粒度。

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionRemSet.cpp

```cpp
void OtherRegionsTable::add_reference(OopOrNarrowOopStar from, int tid) {
  uint cur_hrm_ind = hr()->hrm_index();
  // 计算引用者所在的卡表位置
  int from_card = (int)(uintptr_t(from) >> CardTableModRefBS::card_shift);
  // 为了提高效率，有一个卡表的缓存，在缓存中发现引用已经处理则返回
  if (FromCardCache::contains_or_replace((uint)tid, cur_hrm_ind, from_card)) {
    return;
  }

  // 获取引用者card所在的region index
  HeapRegion* from_hr = _g1h->heap_region_containing_raw(from);
  RegionIdx_t from_hrm_ind = (RegionIdx_t) from_hr->hrm_index();

  // 如果RSet已经变成粗粒度的关系
  // 也就是说RSet里面记录的是引用者对象所在的Region
  // 而不是对象对应的卡表地址，那么可以直接返回
  if (_coarse_map.at(from_hrm_ind)) {
    return;
  }

  // 计算region index
  size_t ind = from_hrm_ind & _mod_max_fine_entries_mask;
  // 找到对应Region的细粒度PRT
  PerRegionTable* prt = find_region_table(ind, from_hr);
  if (prt == NULL) {
    // 加锁避免多个线程同时访问一个Region对应的RSet
    MutexLockerEx x(_m, Mutex::_no_safepoint_check_flag);
    // 再次确认有没有细粒度PRT、针对并发情况
    prt = find_region_table(ind, from_hr);
    if (prt == NULL) {
      // 存储到稀疏PRT
      uintptr_t from_hr_bot_card_index =
        uintptr_t(from_hr->bottom())
          >> CardTableModRefBS::card_shift;
      // 计算card index
      CardIdx_t card_index = from_card - from_hr_bot_card_index;
      // 直接加入稀疏PRT，如果成功则返回，失败则继续执行
      if (G1HRRSUseSparseTable &&
          _sparse_table.add_card(from_hrm_ind, card_index)) {
        return;
      }
      // 细粒度PRT已经满了，删除所有的PRT，然后他们放入粗粒度卡表
      if (_n_fine_entries == _max_fine_entries) {
        prt = delete_region_table();
        prt->init(from_hr, false /* clear_links_to_all_list */);
      } else {
        // 稀疏PRT已经满了，需要分配一个新的细粒度PRT来存储
        prt = PerRegionTable::alloc(from_hr);
        link_to_all(prt);
      }

      PerRegionTable* first_prt = _fine_grain_regions[ind];
      prt->set_collision_list_next(first_prt);
      _fine_grain_regions[ind] = prt;
      _n_fine_entries++;
      // 把稀疏PRT里面的数据迁移到细粒度PRT中，添加成功后删除稀疏PRT
      if (G1HRRSUseSparseTable) {
        SparsePRTEntry *sprt_entry = _sparse_table.get_entry(from_hrm_ind);
        assert(sprt_entry != NULL, "There should have been an entry");
        for (int i = 0; i < SparsePRTEntry::cards_num(); i++) {
          CardIdx_t c = sprt_entry->card(i);
          if (c != SparsePRTEntry::NullEntry) {
            prt->add_card(c);
          }
        }
        bool res = _sparse_table.delete_entry(from_hrm_ind);
        assert(res, "It should have been there.");
      }
    }
    assert(prt != NULL && prt->hr() == from_hr, "consequence");
  }
  assert(prt != NULL, "Inv");
  // 加入prt的位图中，这个位图key是card index
  prt->add_reference(from);

  assert(contains_reference(from), "We just added it!");
}

class PerRegionTable: public CHeapObj<mtGC> {
protected:
  void add_card_work(CardIdx_t from_card, bool par) {
    if (!_bm.at(from_card)) {
      if (par) {
        if (_bm.par_at_put(from_card, 1)) {
          Atomic::inc(&_occupied);
        }
      } else {
        _bm.at_put(from_card, 1);
        _occupied++;
      }
    }
  }

  void add_reference_work(OopOrNarrowOopStar from, bool par) {
    // Must make this robust in case "from" is not in "_hr", because of
    // concurrency.

    if (G1TraceHeapRegionRememberedSet) {
      gclog_or_tty->print_cr("    PRT::Add_reference_work(" PTR_FORMAT "->" PTR_FORMAT").",
                             from,
                             UseCompressedOops
                             ? (void *)oopDesc::load_decode_heap_oop((narrowOop*)from)
                             : (void *)oopDesc::load_decode_heap_oop((oop*)from));
    }

    HeapRegion* loc_hr = hr();
    // If the test below fails, then this table was reused concurrently
    // with this operation.  This is OK, since the old table was coarsened,
    // and adding a bit to the new table is never incorrect.
    // If the table used to belong to a continues humongous region and is
    // now reused for the corresponding start humongous region, we need to
    // make sure that we detect this. Thus, we call is_in_reserved_raw()
    // instead of just is_in_reserved() here.
    if (loc_hr->is_in_reserved_raw(from)) {
      size_t hw_offset = pointer_delta((HeapWord*)from, loc_hr->bottom());
      CardIdx_t from_card = (CardIdx_t)
          hw_offset >> (CardTableModRefBS::card_shift - LogHeapWordSize);

      assert(0 <= from_card && (size_t)from_card < HeapRegion::CardsPerRegion,
             "Must be in range.");
      add_card_work(from_card, par);
    }
  }
public:
  // 被prt->add_reference(from)方法调用
  void add_reference(OopOrNarrowOopStar from) {
    add_reference_work(from, /*parallel*/ true);
  }
}
```