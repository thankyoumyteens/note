# JVMTI

JVM 是不允许在运行时动态重载一个类的, 这表示 Javassist 和 ASM 修改的类需要在原本的类加载之前先被加载。如果要修改已经被 JVM 加载的类, 可以结合 JVMTI 技术一起使用。

JVMTI 是 JVM 提供给“原生工具（C/C++ 程序）”用的底层接口，用来做调试、性能分析、监控等工作。

- 它是 本地（native）接口，不是 Java API
- 运行在 JVM 进程里，和 JVM 几乎是“零距离接触”

很多你熟悉的工具，底层都是基于 JVMTI 做的，例如：

- 各种 profiler（性能分析器）
- 一些 APM/监控探针
- 调试器、内存分析工具

写 JVMTI 工具，通常是：

1. 用 C/C++ 写一个动态库（.so / .dll）
2. 在里面实现 JVM 规定的入口，比如：
   ```cpp
   JNIEXPORT jint JNICALL Agent_OnLoad(JavaVM *vm, char *options, void *reserved) {
       // 获取 JVMTI 环境
       jint res = (*vm)->GetEnv(vm, (void**)&jvmtiEnv, JVMTI_VERSION_1_2);
       // 设置能力（Capabilities）
       // 注册回调（Callbacks）
       // 开启事件
       return JNI_OK;
   }
   ```
3. 启动 JVM 时用：
   ```sh
   java -agentlib:youragent[=options] ...
   ```
4. 在 C 里用 jvmtiEnv 这个指针去调用各种函数，比如：
   - GetAllThreads
   - GetStackTrace
   - IterateThroughHeap
   - AddCapabilities
   - SetEventNotificationMode
   - 等等
