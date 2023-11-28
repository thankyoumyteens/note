# 对 region 进行计数

> jdk8u60-master\hotspot\src\share\vm\gc_implementation\g1\concurrentMark.cpp

```cpp
class G1ParFinalCountTask: public AbstractGangTask {
public:
  void work(uint worker_id) {
    FinalCountDataUpdateClosure final_update_cl(_g1h,
                                                _actual_region_bm,
                                                _actual_card_bm);
    // 对每个region使用FinalCountDataUpdateClosure处理
    if (G1CollectedHeap::use_parallel_gc_threads()) {
      _g1h->heap_region_par_iterate_chunked(&final_update_cl,
                                            worker_id,
                                            _n_workers,
                                            HeapRegion::FinalCountClaimValue);
    } else {
      _g1h->heap_region_iterate(&final_update_cl);
    }
  }
};

class FinalCountDataUpdateClosure: public CMCountDataClosureBase {
public:
  bool doHeapRegion(HeapRegion* hr) {

    if (hr->continuesHumongous()) {
      return false;
    }

    HeapWord* ntams = hr->next_top_at_mark_start();
    HeapWord* top   = hr->top();

    assert(hr->bottom() <= ntams && ntams <= hr->end(), "Preconditions.");

    // 如果在开始并发标记之后又有新的对象分配, 需要额外处理
    if (ntams < top) {
      // 标记该region有存活对象
      set_bit_for_region(hr);

      // 把[nextTAMS, top)范围内新的对象都标记到_card_bm卡表
      BitMap::idx_t start_idx = _cm->card_bitmap_index_for(ntams);
      BitMap::idx_t end_idx = _cm->card_bitmap_index_for(top);

      if (_g1h->is_in_g1_reserved(top) && !_ct_bs->is_card_aligned(top)) {
        end_idx += 1;
      }
      _cm->set_card_bitmap_range(_card_bm, start_idx, end_idx, true /* is_par */);
    }

    // 再次设置标记, 表示这个region有存活的对象
    if (hr->next_marked_bytes() > 0) {
      set_bit_for_region(hr);
    }

    return false;
  }
};
```
