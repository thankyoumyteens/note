# CardSet 容器

```cpp
// --- src/hotspot/share/gc/g1/g1CardSetContainers.hpp --- //

class G1CardSetContainer {
  uintptr_t _ref_count;
protected:
  ~G1CardSetContainer() = default;
public:
  G1CardSetContainer() : _ref_count(3) { }

  uintptr_t refcount() const { return Atomic::load_acquire(&_ref_count); }

  bool try_increment_refcount();

  // Decrement refcount potentially while racing increment, so we need
  // to check the value after attempting to decrement.
  uintptr_t decrement_refcount();

  // Log of largest card index that can be stored in any G1CardSetContainer
  static uint LogCardsPerRegionLimit;

  static uint cards_per_region_limit() { return 1u << LogCardsPerRegionLimit; }
};
```
