# 释放容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSet.cpp --- //

void G1CardSet::release_and_maybe_free_container(ContainerPtr container) {
    // 释放容器(就是减少_ref_count的值)
    if (release_container(container)) {
        // 释放内存
        free_mem_object(container);
    }
}

bool G1CardSet::release_container(ContainerPtr container) {
    uint cs_type = container_type(container);
    // FullCardSet和ContainerInlinePtr都只是指针, 无需释放
    if (container == FullCardSet || cs_type == ContainerInlinePtr) {
        return false;
    }

    // _ref_count减2
    G1CardSetContainer *container_on_heap = (G1CardSetContainer *) strip_container_type(container);
    return container_on_heap->decrement_refcount() == 1;
}

void G1CardSet::free_mem_object(ContainerPtr container) {
    assert(container != G1CardSet::FreeCardSet, "should not free container FreeCardSet");
    assert(container != G1CardSet::FullCardSet, "should not free container FullCardSet");

    uintptr_t type = container_type(container);
    void *value = strip_container_type(container);

    assert(type == G1CardSet::ContainerArrayOfCards ||
           type == G1CardSet::ContainerBitMap ||
           type == G1CardSet::ContainerHowl, "should not free card set type %zu", type);
    assert(static_cast<G1CardSetContainer *>(value)->refcount() == 1, "must be");

    _mm->free(container_type_to_mem_object_type(type), value);
}
```
