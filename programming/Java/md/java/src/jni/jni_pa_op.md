# JNI 操作基本类型的数组

## 获取数组长度

```cpp
jsize GetArrayLength(jarray array);
```

## 把 java 的基本类型数组转换成 c++ 的数组

```cpp
jboolean * GetBooleanArrayElements(jbooleanArray array, jboolean *isCopy);
jbyte * GetByteArrayElements(jbyteArray array, jboolean *isCopy);
jchar * GetCharArrayElements(jcharArray array, jboolean *isCopy);
jshort * GetShortArrayElements(jshortArray array, jboolean *isCopy);
jint * GetIntArrayElements(jintArray array, jboolean *isCopy);
jlong * GetLongArrayElements(jlongArray array, jboolean *isCopy);
jfloat * GetFloatArrayElements(jfloatArray array, jboolean *isCopy);
jdouble * GetDoubleArrayElements(jdoubleArray array, jboolean *isCopy);
```

## 释放 c++ 数组

必须与 GetXXXXXXArrayElements 配对使用，以确保资源正确释放和数据同步。

```cpp
void ReleaseBooleanArrayElements(jbooleanArray array, jboolean *elems, jint mode);
void ReleaseByteArrayElements(jbyteArray array, jbyte *elems, jint mode);
void ReleaseCharArrayElements(jcharArray array, jchar *elems, jint mode);
void ReleaseShortArrayElements(jshortArray array, jshort *elems, jint mode);
void ReleaseIntArrayElements(jintArray array, jint *elems, jint mode);
void ReleaseLongArrayElements(jlongArray array, jlong *elems, jint mode);
void ReleaseFloatArrayElements(jfloatArray array, jfloat *elems, jint mode);
void ReleaseDoubleArrayElements(jdoubleArray array, jdouble *elems, jint mode);
```

mode: 释放模式，指定 JVM 如何处理 c++ 代码对数组所做的修改。可选值为:

- 0: 将 c++ 修改复制回 Java 数组，并释放 c++ 数组
- JNI_COMMIT: 将 c++ 修改复制回 Java 数组，但不释放资源（可继续使用指针）
- JNI_ABORT: 忽略 c++ 修改，直接释放资源，Java 数组内容保持不变

## 从 java 数组中复制指定范围的元素到 c++ 数组中

```cpp
void GetBooleanArrayRegion(jbooleanArray array, jsize start, jsize len, jboolean *buf);
void GetByteArrayRegion(jbyteArray array, jsize start, jsize len, jbyte *buf);
void GetCharArrayRegion(jcharArray array, jsize start, jsize len, jchar *buf);
void GetShortArrayRegion(jshortArray array, jsize start, jsize len, jshort *buf);
void GetIntArrayRegion(jintArray array, jsize start, jsize len, jint *buf);
void GetLongArrayRegion(jlongArray array, jsize start, jsize len, jlong *buf);
void GetFloatArrayRegion(jfloatArray array, jsize start, jsize len, jfloat *buf);
void GetDoubleArrayRegion(jdoubleArray array, jsize start, jsize len, jdouble *buf);
```

## 从 c++ 数组中复制指定范围的元素到 java 数组中

```cpp
void SetBooleanArrayRegion(jbooleanArray array, jsize start, jsize len, const jboolean *buf);
void SetByteArrayRegion(jbyteArray array, jsize start, jsize len, jbyte *buf);
void SetCharArrayRegion(jcharArray array, jsize start, jsize len, jchar *buf);
void SetShortArrayRegion(jshortArray array, jsize start, jsize len, jshort *buf);
void SetIntArrayRegion(jintArray array, jsize start, jsize len, jint *buf);
void SetLongArrayRegion(jlongArray array, jsize start, jsize len, jlong *buf);
void SetFloatArrayRegion(jfloatArray array, jsize start, jsize len, jfloat *buf);
void SetDoubleArrayRegion(jdoubleArray array, jsize start, jsize len, jdouble *buf);
```

## 创建一个 java 数组

```cpp
jbooleanArray NewBooleanArray(jsize len);
jbooleanArray NewByteArray(jsize len);
jbooleanArray NewCharArray(jsize len);
jbooleanArray NewShortArray(jsize len);
jbooleanArray NewIntArray(jsize len);
jbooleanArray NewLongArray(jsize len);
jbooleanArray NewFloatArray(jsize len);
jbooleanArray NewDoubleArray(jsize len);
```

## 获取 java 基本类型数组的直接指针

允许 c++ 代码在不进行数据复制的情况下直接操作 Java 数组。

```cpp
void * GetPrimitiveArrayCritical(jarray array, jboolean *isCopy);
```

## 释放 java 基本类型数组的直接指针

这个函数必须与 GetPrimitiveArrayCritical 配对使用，以确保 JVM 能够恢复对数组内存的正常管理。

```cpp
void ReleasePrimitiveArrayCritical(jarray array, void *carray, jint mode);
```

## 临界区(Critical)的限制

在临界区内（即调用 GetPrimitiveArrayCritical 之后、ReleasePrimitiveArrayCritical 之前），c++ 代码不能调用可能导致线程阻塞或触发垃圾回收的 JNI 函数，也不能执行可能阻塞 JVM 的操作。

临界区应该尽可能短，以减少 JVM 被阻塞的时间。
