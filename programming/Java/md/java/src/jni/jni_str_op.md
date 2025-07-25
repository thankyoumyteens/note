# JNI 操作字符串

## 将 Java 字符串转换为以 `\0` 结尾的 UTF-8 编码的 C 字符串

```cpp
const char* GetStringUTFChars(jstring str, jboolean *isCopy);
```

isCopy: 指向一个 jboolean 变量的指针。如果为 JNI_TRUE，表示返回的 C 字符串是原始 Java 字符串的副本；如果为 JNI_FALSE，表示返回的是指向内部数据的直接指针。isCopy 参数的值由 JVM 设置。

## 释放通过 GetStringUTFChars 获取的 UTF-8 编码的 C 字符串

这个函数必须与 GetStringUTFChars 配对使用，以确保资源正确释放和内存安全。

```cpp
void ReleaseStringUTFChars(jstring str, const char* chars);
```

如果 JVM 在调用 GetStringUTFChars 时复制了原始 Java 字符串（由 isCopy 参数指示），则 ReleaseStringUTFChars 会确保这些临时内存被正确回收。如果返回的是直接指针，则该函数会通知 JVM 本地代码不再需要访问该指针。

## 根据 UTF-8 编码的 C 字符串创建一个新的 Java 字符串对象

```cpp
jstring NewStringUTF(const char *utf);
```

## 获取 java 字符串转换为 UTF-8 编码后的字节长度

这个函数返回的长度不包括字符串结尾的 `\0`。

```cpp
jsize GetStringUTFLength(jstring str);
```

## 将 Java 字符串的指定区域转换为 UTF-8 编码，并复制到预先分配的 C 字符数组中

这个函数允许你选择性地提取 Java 字符串的一部分内容，而不是整个字符串。

```cpp
void GetStringUTFRegion(jstring str, jsize start, jsize len, char *buf);
```

- str: Java 字符串对象的引用，要提取内容的目标字符串
- start: 起始索引（从 0 开始），指定从 Java 字符串的哪个位置开始提取
- len: 要提取的字符数量
- buf: 指向预先分配的 C 字符数组的指针，用于存储转换后的 UTF-8 字符串

## UTF-16 版本

```cpp
const jchar *GetStringChars(jstring str, jboolean *isCopy);
void ReleaseStringChars(jstring str, const jchar *chars);
jstring NewString(const jchar *unicode, jsize len);
jsize GetStringLength(jstring str);
void GetStringRegion(jstring str, jsize start, jsize len, jchar *buf);
```

## 获取 Java 字符串的 UTF-16 编码表示的直接指针

允许 c++ 代码直接访问 java 字符串内容而无需进行复制。

与 GetStringChars 相比，GetStringCritical 提供了一种更高效但更受限制的方式来访问字符串内容，适用于需要最小化 JVM 阻塞时间的高性能场景。

```cpp
const jchar * GetStringCritical(jstring string, jboolean *isCopy);
```

## 用于释放通过 GetStringCritical 获取的 UTF-16 编码字符串指针

这个函数必须与 GetStringCritical 配对使用，以确保 JVM 能够恢复对字符串内存的正常管理。

```cpp
void ReleaseStringCritical(jstring string, const jchar *cstring);
```

## 临界区(Critical)的限制

在临界区内（即调用 GetPrimitiveArrayCritical 之后、ReleasePrimitiveArrayCritical 之前），c++ 代码不能调用可能导致线程阻塞或触发垃圾回收的 JNI 函数，也不能执行可能阻塞 JVM 的操作。

临界区应该尽可能短，以减少 JVM 被阻塞的时间。
