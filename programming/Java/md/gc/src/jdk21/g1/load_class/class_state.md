# 类的状态

```cpp
// --- src/hotspot/share/oops/instanceKlass.hpp.InstanceKlass --- //

enum ClassState : u1 {
  allocated,                          // allocated (but not yet linked)
  loaded,                             // loaded and inserted in class hierarchy (but not linked yet)
  being_linked,                       // currently running verifier and rewriter
  linked,                             // successfully linked/verified (but not initialized yet)
  being_initialized,                  // currently running class initializer
  fully_initialized,                  // initialized (successful final state)
  initialization_error                // error happened during initialization
};
```
