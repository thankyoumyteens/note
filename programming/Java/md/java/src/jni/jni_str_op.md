# JNI 字符串操作

如果使用 c++方式调用, 则第一个参数 `JNIEnv *env` 不需要传, 比如: `const char *inCStr = env->GetStringUTFChars(inJNIStr, NULL);`。

UTF-8 编码的字符串(1~3 字节)

```cpp
// java字符串转char数组
// isCopy 由JVM设置
const char * GetStringUTFChars(JNIEnv *env, jstring string, jboolean *isCopy);

// 释放对字符串string的引用, 让它可以被GC
void ReleaseStringUTFChars(JNIEnv *env, jstring string, const char *utf);

// char数组转java字符串
jstring NewStringUTF(JNIEnv *env, const char *bytes);

// 获取字符串的长度
jsize GetStringUTFLength(JNIEnv *env, jstring string);

// 截取字符串保存到buf中
void GetStringUTFRegion(JNIEnv *env, jstring str, jsize start, jsize length, char *buf);
```

Unicode 编码的字符串(4 字节)

```cpp
// java字符串转char数组
const jchar * GetStringChars(JNIEnv *env, jstring string, jboolean *isCopy);

// 释放对字符串string的引用
void ReleaseStringChars(JNIEnv *env, jstring string, const jchar *chars);

// char数组转java字符串
jstring NewString(JNIEnv *env, const jchar *unicodeChars, jsize length);

// 获取字符串的长度
jsize GetStringLength(JNIEnv *env, jstring string);

// 截取字符串保存到buf中
void GetStringRegion(JNIEnv *env, jstring str, jsize start, jsize length, jchar *buf);

// java字符串转char数组(进入临界区)
// 在调用ReleaseStringCritical之前, 不能有任何阻塞当前线程的操作
jchar * GetStringCritical(JNIEnv *env, jstring string, jboolean *isCopy);

// 退出临界区
void ReleaseStringCritical(JNIEnv *env, jstring string, const jchar *cstring);
```

## GetStringChars/GetStringRegion/GetStringCritical

这三个函数的作用都一样，都是将 Java 的 String 对像，转换为 char 数组。JVM 在返回 char 数组时有两个选择:

1. 将 java String 所对应的原始 jchar 拷贝一份返回，并将 isCopy 赋值为 true。函数返回的指针指向一份拷贝的数据，即使修改也不会对原始字符串造成影响
2. 将 Java String 所对应的原始 jchar 直接返回，并将 isCopy 赋值为 false。函数返回的指针指向原始数据，修改会直接改动原始字符串

GetStringChar 和 GetStringCritical 的区别在于: GetStringCritical 返回原始字符串的可能性更高, 一般情况下，GetStringChar 返回的是一份拷贝。GetStringCritical 返回的是原始字符串。

注意： 在 GetStringCritical 和 ReleaseStringCritical 函数之间不能再调用其他任何 JNI 函数，也不能有任何阻塞当前线程的操作。
