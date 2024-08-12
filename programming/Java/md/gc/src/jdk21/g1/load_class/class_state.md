# 类的状态

```cpp
// --- src/hotspot/share/oops/instanceKlass.hpp.InstanceKlass --- //

enum ClassState : u1 {
  allocated,           // 已分配, 还没链接
  loaded,              // 加载完成
  being_linked,        // 正在链接
  linked,              // 链接完成, 还没初始化
  being_initialized,   // 正在初始化
  fully_initialized,   // 完成初始化
  initialization_error // 初始化过程中出错
};
```
