# 调用 java 主方法

在 JavaMain 中, 虚拟机得到初始化之后, 接下来就将执行应用程序的主方法。通过 env 调用 CallStaticVoidMethod 函数, 可以执行一个由“static”和“void”修饰的方法, 即 Java 应用程序主类的 main 方法。

```cpp
// --- src/java.base/share/native/libjli/java.c --- //

mainID = (*env)->GetStaticMethodID(env, mainClass, "main",
                                    "([Ljava/lang/String;)V");
CHECK_EXCEPTION_NULL_LEAVE(mainID);
(*env)->CallStaticVoidMethod(env, mainClass, mainID, mainArgs);
break;
```

CallStaticVoidMethod 指向 jni_CallStaticVoidMethod 函数。

为了执行主类的 main 方法, 将在 jni_invoke_static 中通过调用 JavaCalls 模块完成 Java 方法的执行。在 HotSpot 中, 所有对 Java 方法的调用都需要通过 JavaCalls 类来完成。

```cpp
// --- src/hotspot/share/prims/jni.cpp --- //

JNI_ENTRY(void, jni_CallStaticVoidMethod(JNIEnv *env, jclass cls, jmethodID methodID, ...))
  HOTSPOT_JNI_CALLSTATICVOIDMETHOD_ENTRY(env, cls, (uintptr_t) methodID);
  DT_VOID_RETURN_MARK(CallStaticVoidMethod);

  va_list args;
  va_start(args, methodID);
  JavaValue jvalue(T_VOID);
  JNI_ArgumentPusherVaArg ap(methodID, args);
  jni_invoke_static(env, &jvalue, nullptr, JNI_STATIC, methodID, &ap, CHECK);
  va_end(args);
JNI_END

static void jni_invoke_static(JNIEnv *env, JavaValue* result, jobject receiver, JNICallType call_type, jmethodID method_id, JNI_ArgumentPusher *args, TRAPS) {
  // 根据method id转换成方法句柄
  methodHandle method(THREAD, Method::resolve_jmethod_id(method_id));

  // Create object to hold arguments for the JavaCall, and associate it with
  // the jni parser
  ResourceMark rm(THREAD);
  int number_of_parameters = method->size_of_parameters();
  JavaCallArguments java_args(number_of_parameters);

  assert(method->is_static(), "method should be static");

  // Fill out JavaCallArguments object
  args->push_arguments_on(&java_args);
  // Initialize result type
  result->set_type(args->return_type());

  // Invoke the method. Result is returned as oop.
  // 调用JavaCalls的call方法实现从JVM对Java方法的调用
  JavaCalls::call(result, method, &java_args, CHECK);

  // Convert result
  if (is_reference_type(result->get_type())) {
    result->set_jobject(JNIHandles::make_local(THREAD, result->get_oop()));
  }
}
```
