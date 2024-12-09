# 疏散回收集后阶段

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::post_evacuate_collection_set(G1EvacInfo *evacuation_info,
                                                    G1ParScanThreadStateSet *per_thread_states) {
    G1GCPhaseTimes *p = phase_times();

    // Process any discovered reference objects - we have
    // to do this _before_ we retire the GC alloc regions
    // as we may have to copy some 'reachable' referent
    // objects (and their reachable sub-graphs) that were
    // not copied during the pause.
    process_discovered_references(per_thread_states);

    G1STWIsAliveClosure is_alive(_g1h);
    G1KeepAliveClosure keep_alive(_g1h);

    WeakProcessor::weak_oops_do(workers(), &is_alive, &keep_alive, p->weak_phase_times());

    allocator()->release_gc_alloc_regions(evacuation_info);

    post_evacuate_cleanup_1(per_thread_states);

    post_evacuate_cleanup_2(per_thread_states, evacuation_info);

    _evac_failure_regions.post_collection();

    assert_used_and_recalculate_used_equal(_g1h);

    _g1h->rebuild_free_region_list();

    _g1h->record_obj_copy_mem_stats();

    evacuation_info->set_bytes_used(_g1h->bytes_used_during_gc());

    _g1h->prepare_for_mutator_after_young_collection();

    _g1h->gc_epilogue(false);

    _g1h->expand_heap_after_young_collection();
}
```
