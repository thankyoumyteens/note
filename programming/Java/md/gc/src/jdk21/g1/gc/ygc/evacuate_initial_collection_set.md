# 实际执行回收

```cpp
// --- src/hotspot/share/gc/g1/g1YoungCollector.cpp --- //

void G1YoungCollector::evacuate_initial_collection_set(G1ParScanThreadStateSet *per_thread_states,
                                                       bool has_optional_evacuation_work) {
    G1GCPhaseTimes *p = phase_times();

    {
        Ticks start = Ticks::now();
        rem_set()->merge_heap_roots(true /* initial_evacuation */);
        p->record_merge_heap_roots_time((Ticks::now() - start).seconds() * 1000.0);
    }

    Tickspan task_time;
    const uint num_workers = workers()->active_workers();

    Ticks start_processing = Ticks::now();
    {
        G1RootProcessor root_processor(_g1h, num_workers);
        G1EvacuateRegionsTask g1_par_task(_g1h,
                                          per_thread_states,
                                          task_queues(),
                                          &root_processor,
                                          num_workers,
                                          has_optional_evacuation_work);
        task_time = run_task_timed(&g1_par_task);
        // Closing the inner scope will execute the destructor for the
        // G1RootProcessor object. By subtracting the WorkerThreads task from the total
        // time of this scope, we get the "NMethod List Cleanup" time. This list is
        // constructed during "STW two-phase nmethod root processing", see more in
        // nmethod.hpp
    }
    Tickspan total_processing = Ticks::now() - start_processing;

    p->record_initial_evac_time(task_time.seconds() * 1000.0);
    p->record_or_add_nmethod_list_cleanup_time((total_processing - task_time).seconds() * 1000.0);

    rem_set()->complete_evac_phase(has_optional_evacuation_work);
}
```
