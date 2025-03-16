# 指针队列

```cpp
class PtrQueue {

    // 最后一个入队的元素的下标
    size_t _index;

    // 队列的容量
    size_t _capacity_in_bytes;

    // 队列中每个元素的大小就是一个指针的大小
    static const size_t _element_size = sizeof(void *);

protected:
    // The buffer.
    void **_buf;

    // Initialize this queue to contain a null buffer, and be part of the
    // given PtrQueueSet.
    PtrQueue(PtrQueueSet *qset);

    // Requires queue flushed.
    ~PtrQueue();
};
```
