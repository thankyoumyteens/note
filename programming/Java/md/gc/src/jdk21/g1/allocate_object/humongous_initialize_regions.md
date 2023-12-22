# 初始化region空间

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

  // The passed in hr will be the "starts humongous" region. The header
  // of the new object will be placed at the bottom of this region.
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
  Copy::fill_to_words(new_obj, oopDesc::header_size(), 0);

  // Next, update the metadata for the regions.
  set_humongous_metadata(first_hr, num_regions, word_size, true);

  HeapRegion* last_hr = region_at(last);
  size_t used = byte_size(first_hr->bottom(), last_hr->top());

  increase_used(used);

  for (uint i = first; i <= last; ++i) {
    HeapRegion *hr = region_at(i);
    _humongous_set.add(hr);
    _hr_printer.alloc(hr);
  }

  return new_obj;
}
```
