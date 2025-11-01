# JNIEXPORT 宏

在 Darwin/macOS 平台中, JNIEXPORT 宏定义如下:

```c
#define JNIEXPORT     __attribute__((visibility("default")))
```

JNIEXPORT 宏，用于指定 JNI 函数的符号可见性。

符号可见性是操作系统和编译器提供的一种机制，用于控制共享库中的函数和变量是否可以被库外部的代码访问：

- 可见符号：可以被库外部代码调用或引用
- 不可见符号：仅能在库内部使用，外部不可见

`__attribute__((visibility("default")))` 是 GCC/Clang 编译器的一个特性，具体含义为：

- 设置函数/变量的可见性级别为 "default"
- 在共享库（如 `.dylib` 文件）中，被此属性标记的函数将**对外可见**，可以被库外部的代码调用
- 这是 Darwin/macOS 平台上控制符号导出的标准方式

## JNI 上下文的重要性

在 JNI 环境中，这个宏的作用尤为关键：

- 它确保 Java 虚拟机能够正确识别和调用原生方法
- 当 Java 代码通过 `native` 关键字声明本地方法并通过 `System.loadLibrary()` 加载本地库时，JVM 依赖这些可见的符号来解析函数调用
- 没有正确标记可见性的 JNI 函数会导致 `UnsatisfiedLinkError` 错误

## 不同平台上的实现方式

符号可见性在不同平台上有不同的实现方式：

- Darwin/macOS：使用 `__attribute__((visibility("default")))`
- Windows：通常使用 `__declspec(dllexport)`
- Linux：可以使用 `__attribute__((visibility("default")))` 或链接器脚本
