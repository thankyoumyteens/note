# RSet 清理

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.cpp

```cpp
class G1ParScrubRemSetTask: public AbstractGangTask {
public:
  void work(uint worker_id) {
    if (G1CollectedHeap::use_parallel_gc_threads()) {
      _g1rs->scrub_par(_region_bm, _card_bm, worker_id,
                       HeapRegion::ScrubRemSetClaimValue);
    } else {
      _g1rs->scrub(_region_bm, _card_bm);
    }
  }

};
```

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\heapRegionRemSet.cpp

```cpp
void OtherRegionsTable::scrub(CardTableModRefBS* ctbs,
                              BitMap* region_bm, BitMap* card_bm) {
  assert(_coarse_map.size() == region_bm->size(), "Precondition");
  _coarse_map.set_intersection(*region_bm);
  _n_coarse_entries = _coarse_map.count_one_bits();

  for (size_t i = 0; i < _max_fine_entries; i++) {
    PerRegionTable* cur = _fine_grain_regions[i];
    PerRegionTable** prev = &_fine_grain_regions[i];
    while (cur != NULL) {
      PerRegionTable* nxt = cur->collision_list_next();
      if (!region_bm->at((size_t) cur->hr()->hrm_index())) {
        *prev = nxt;
        cur->set_collision_list_next(NULL);
        _n_fine_entries--;
        unlink_from_all(cur);
        PerRegionTable::free(cur);
      } else {
        cur->scrub(ctbs, card_bm);
        if (cur->occupied() == 0) {
          *prev = nxt;
          cur->set_collision_list_next(NULL);
          _n_fine_entries--;
          unlink_from_all(cur);
          PerRegionTable::free(cur);
        } else {
          prev = cur->collision_list_next_addr();
        }
      }
      cur = nxt;
    }
  }
  clear_fcc();
}
```
