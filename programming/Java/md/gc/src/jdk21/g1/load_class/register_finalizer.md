# 注册 finalizer

```cpp
//////////////////////////////////////////////////////////////////////////
// src/hotspot/share/interpreter/interpreterRuntime.cpp //
//////////////////////////////////////////////////////////////////////////

instanceOop InstanceKlass::register_finalizer(instanceOop i, TRAPS) {
  // 打印注册finalizer相关日志
  if (TraceFinalizerRegistration) {
    tty->print("Registered ");
    i->print_value_on(tty);
    tty->print_cr(" (" PTR_FORMAT ") as finalizable", p2i(i));
  }
  instanceHandle h_i(THREAD, i);
  // Pass the handle as argument, JavaCalls::call expects oop as jobjects
  JavaValue result(T_VOID);
  JavaCallArguments args(h_i);
  methodHandle mh(THREAD, Universe::finalizer_register_method());
  JavaCalls::call(&result, mh, &args, CHECK_NULL);
  MANAGEMENT_ONLY(FinalizerService::on_register(h_i(), THREAD);)
  return h_i();
}
```
