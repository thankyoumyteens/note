# 从 TLAB 中分配对象

TLAB 使用指针碰撞分配内存: 所有被使用过的内存都被放在一边, 空闲的内存被放在另一边, 中间放着一个指针作为分界点的指示器, 分配内存就仅仅是把指针向空闲空间方向挪动一段与对象大小相等的距离。

HeapWord 是 JVM 管理的堆内存的地址抽象。堆中的内存地址都需要通过 HeapWord* 指针进行表示, 例如申请内存起始地址的函数一般返回的都是 HeapWord*, 大小也是 HeapWordSize 的整数倍, 因为 Java 堆是按照一定内存大小对齐的。

```cpp
// jdk21-jdk-21-ga/src/hotspot/share/gc/shared/threadLocalAllocBuffer.inline.hpp
inline HeapWord* ThreadLocalAllocBuffer::allocate(size_t size) {
  // void invariants() const {
  //   assert(top() >= start() && top() <= end(), "invalid tlab");
  // }
  invariants();
  // TLAB的范围: _start ~ _end
  // 已分配的区域: _start ~ _top
  // 未分配的区域: _top ~ _end
  HeapWord* obj = top();
  // 判断TLAB剩余空间够不够分配这个对象
  if (pointer_delta(end(), obj) >= size) {
    // TLAB剩余空间大于这个对象所需的空间
#ifdef ASSERT
    // Skip mangling the space corresponding to the object header to
    // ensure that the returned space is not considered parsable by
    // any concurrent GC thread.
    size_t hdr_size = oopDesc::header_size();
    Copy::fill_to_words(obj + hdr_size, size - hdr_size, badHeapWordVal);
#endif // ASSERT
    // 移动_top指针, 增加这个对象大小
    set_top(obj + size);

    invariants();
    return obj;
  }
  return nullptr;
}

// jdk21-jdk-21-ga/src/hotspot/share/utilities/globalDefinitions.hpp
inline size_t pointer_delta(const HeapWord* left, const HeapWord* right) {
  return pointer_delta(left, right, sizeof(HeapWord));
}

inline size_t pointer_delta(const volatile void* left,
                            const volatile void* right,
                            size_t element_size) {
  assert(left >= right, "avoid underflow - left: " PTR_FORMAT " right: " PTR_FORMAT, p2i(left), p2i(right));
  // 计算left和right之间有多少个HeapWord
  return (((uintptr_t) left) - ((uintptr_t) right)) / element_size;
}
```
