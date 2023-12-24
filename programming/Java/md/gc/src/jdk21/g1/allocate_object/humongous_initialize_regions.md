# 初始化 region 空间

```cpp
/////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1CollectedHeap.cpp //
/////////////////////////////////////////////////////////////////

HeapWord*
G1CollectedHeap::humongous_obj_allocate_initialize_regions(HeapRegion* first_hr,
                                                           uint num_regions,
                                                           size_t word_size) {
  assert(first_hr != nullptr, "pre-condition");
  assert(is_humongous(word_size), "word_size should be humongous");
  assert(num_regions * HeapRegion::GrainWords >= word_size, "pre-condition");

  // 大对象所在的第一个region和最后一个region的索引
  uint first = first_hr->hrm_index();
  uint last = first + num_regions - 1;

  // We need to initialize the region(s) we just discovered. This is
  // a bit tricky given that it can happen concurrently with
  // refinement threads refining cards on these regions and
  // potentially wanting to refine the BOT as they are scanning
  // those cards (this can happen shortly after a cleanup; see CR
  // 6991377). So we have to set up the region(s) carefully and in
  // a specific order.

  // 大对象的起始region
  // 从bottom指针处开始分配对象头
  HeapWord* new_obj = first_hr->bottom();

  // First, we need to zero the header of the space that we will be
  // allocating. When we update top further down, some refinement
  // threads might try to scan the region. By zeroing the header we
  // ensure that any thread that will try to scan the region will
  // come across the zero klass word and bail out.
  //
  // NOTE: It would not have been correct to have used
  // CollectedHeap::fill_with_object() and make the space look like
  // an int array. The thread that is doing the allocation will
  // later update the object header to a potentially different array
  // type and, for a very short period of time, the klass and length
  // fields will be inconsistent. This could cause a refinement
  // thread to calculate the object size incorrectly.
  // 把对象头的内存初始化为0
  Copy::fill_to_words(new_obj, oopDesc::header_size(), 0);

  // Next, update the metadata for the regions.
  set_humongous_metadata(first_hr, num_regions, word_size, true);

  // 大对象的最后一个region
  HeapRegion* last_hr = region_at(last);
  // 计算大对象占用多大内存
  size_t used = byte_size(first_hr->bottom(), last_hr->top());

  increase_used(used);

  for (uint i = first; i <= last; ++i) {
    HeapRegion *hr = region_at(i);
    _humongous_set.add(hr);
    _hr_printer.alloc(hr);
  }

  return new_obj;
}

void G1CollectedHeap::set_humongous_metadata(HeapRegion* first_hr,
                                             uint num_regions,
                                             size_t word_size,
                                             bool update_remsets) {
  // 计算top指针的位置(大对象末尾的位置)
  HeapWord* obj_top = first_hr->bottom() + word_size;
  // 计算大对象分配的region的大小
  size_t word_size_sum = num_regions * HeapRegion::GrainWords;
  assert(word_size <= word_size_sum, "sanity");

  // How many words memory we "waste" which cannot hold a filler object.
  size_t words_not_fillable = 0;

  // Pad out the unused tail of the last region with filler
  // objects, for improved usage accounting.

  // How many words can we use for filler objects.
  size_t words_fillable = word_size_sum - word_size;

  if (words_fillable >= G1CollectedHeap::min_fill_size()) {
    G1CollectedHeap::fill_with_objects(obj_top, words_fillable);
  } else {
    // We have space to fill, but we cannot fit an object there.
    words_not_fillable = words_fillable;
    words_fillable = 0;
  }

  // We will set up the first region as "starts humongous". This
  // will also update the BOT covering all the regions to reflect
  // that there is a single object that starts at the bottom of the
  // first region.
  first_hr->hr_clear(false /* clear_space */);
  first_hr->set_starts_humongous(obj_top, words_fillable);

  if (update_remsets) {
    _policy->remset_tracker()->update_at_allocate(first_hr);
  }

  // Indices of first and last regions in the series.
  uint first = first_hr->hrm_index();
  uint last = first + num_regions - 1;

  HeapRegion* hr = nullptr;
  for (uint i = first + 1; i <= last; ++i) {
    hr = region_at(i);
    hr->hr_clear(false /* clear_space */);
    hr->set_continues_humongous(first_hr);
    if (update_remsets) {
      _policy->remset_tracker()->update_at_allocate(hr);
    }
  }

  // Up to this point no concurrent thread would have been able to
  // do any scanning on any region in this series. All the top
  // fields still point to bottom, so the intersection between
  // [bottom,top] and [card_start,card_end] will be empty. Before we
  // update the top fields, we'll do a storestore to make sure that
  // no thread sees the update to top before the zeroing of the
  // object header and the BOT initialization.
  OrderAccess::storestore();

  // Now, we will update the top fields of the "continues humongous"
  // regions except the last one.
  for (uint i = first; i < last; ++i) {
    hr = region_at(i);
    hr->set_top(hr->end());
  }

  hr = region_at(last);
  // If we cannot fit a filler object, we must set top to the end
  // of the humongous object, otherwise we cannot iterate the heap
  // and the BOT will not be complete.
  hr->set_top(hr->end() - words_not_fillable);

  assert(hr->bottom() < obj_top && obj_top <= hr->end(),
         "obj_top should be in last region");

  assert(words_not_fillable == 0 ||
         first_hr->bottom() + word_size_sum - words_not_fillable == hr->top(),
         "Miscalculation in humongous allocation");
}

////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/heapRegion.cpp //
////////////////////////////////////////////////////////////

void HeapRegion::hr_clear(bool clear_space) {
  set_top(bottom());
  clear_young_index_in_cset();
  clear_index_in_opt_cset();
  uninstall_surv_rate_group();
  set_free();
  reset_pre_dummy_top();

  rem_set()->clear_locked();

  init_top_at_mark_start();
  if (clear_space) clear(SpaceDecorator::Mangle);
}

void HeapRegion::set_starts_humongous(HeapWord* obj_top, size_t fill_size) {
  assert(!is_humongous(), "sanity / pre-condition");
  assert(top() == bottom(), "should be empty");
  // 发送通知
  report_region_type_change(G1HeapRegionTraceType::StartsHumongous);
  _type.set_starts_humongous();
  _humongous_start_region = this;

  _bot_part.set_for_starts_humongous(obj_top, fill_size);
}
```
