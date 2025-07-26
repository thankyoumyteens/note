# JNI 操作方法

在 JNI 中访问方法的步骤:

1. 通过 GetObjectClass 获取 java 对象所属的类
2. 通过 GetMethodID, 根据方法名和方法的签名, 获取类中指定方法的 ID
3. 根据方法的 ID 调用 CallXXXXXXMethod 调用 java 方法

```cpp
jmethodID GetMethodID(jclass clazz, const char *name, const char *sig);
jmethodID GetStaticMethodID(jclass clazz, const char *name, const char *sig);
```

## 在 c++ 中调用 Java 对象的实例方法

```cpp
jobject CallObjectMethod(jobject obj, jmethodID methodID, ...);
jboolean CallBooleanMethod(jobject obj, jmethodID methodID, ...);
jbyte CallByteMethod(jobject obj, jmethodID methodID, ...);
jchar CallCharMethod(jobject obj, jmethodID methodID, ...);
jshort CallShortMethod(jobject obj, jmethodID methodID, ...);
jint CallIntMethod(jobject obj, jmethodID methodID, ...);
jlong CallLongMethod(jobject obj, jmethodID methodID, ...);
jfloat CallFloatMethod(jobject obj, jmethodID methodID, ...);
jdouble CallDoubleMethod(jobject obj, jmethodID methodID, ...);
void CallVoidMethod(jobject obj, jmethodID methodID, ...);
```

这个函数与 CallXXXXXMethod 类似，但它使用一个 jvalue 数组来传递参数，而不是可变参数列表，这使得它在参数数量或类型不确定的情况下更加灵活

```cpp
jobject CallObjectMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jboolean CallBooleanMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jbyte CallByteMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jchar CallCharMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jshort CallShortMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jint CallIntMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jlong CallLongMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jfloat CallFloatMethodA(jobject obj, jmethodID methodID, const jvalue * args);
jdouble CallDoubleMethodA(jobject obj, jmethodID methodID, const jvalue * args);
void CallVoidMethodA(jobject obj, jmethodID methodID, const jvalue * args);
```

jvalue 是一个联合类型，用于表示各种 JNI 类型的值

```cpp
typedef union jvalue {
    jboolean z;
    jbyte    b;
    jchar    c;
    jshort   s;
    jint     i;
    jlong    j;
    jfloat   f;
    jdouble  d;
    jobject  l;
} jvalue;
```

这个函数与 CallXXXXXMethod 和 CallXXXXXMethodA 类似，但它使用 va_list 可变参数列表，这使得它在参数传递方式上更加灵活，适用于需要动态构建参数列表的场景

```cpp
jobject CallObjectMethodV(jobject obj, jmethodID methodID, va_list args);
jboolean CallBooleanMethodV(jobject obj, jmethodID methodID, va_list args);
jbyte CallByteMethodV(jobject obj, jmethodID methodID, va_list args);
jchar CallCharMethodV(jobject obj, jmethodID methodID, va_list args);
jshort CallShortMethodV(jobject obj, jmethodID methodID, va_list args);
jint CallIntMethodV(jobject obj, jmethodID methodID, va_list args);
jlong CallLongMethodV(jobject obj, jmethodID methodID, va_list args);
jfloat CallFloatMethodV(jobject obj, jmethodID methodID, va_list args);
jdouble CallDoubleMethodV(jobject obj, jmethodID methodID, va_list args);
void CallVoidMethodV(jobject obj, jmethodID methodID, va_list args);
```

## 在 c++ 中调用 Java 类的静态方法

```cpp
jobject CallObjectMethod(jclass clazz, jmethodID methodID, ...);
jboolean CallBooleanMethod(jclass clazz, jmethodID methodID, ...);
jbyte CallByteMethod(jclass clazz, jmethodID methodID, ...);
jchar CallCharMethod(jclass clazz, jmethodID methodID, ...);
jshort CallShortMethod(jclass clazz, jmethodID methodID, ...);
jint CallIntMethod(jclass clazz, jmethodID methodID, ...);
jlong CallLongMethod(jclass clazz, jmethodID methodID, ...);
jfloat CallFloatMethod(jclass clazz, jmethodID methodID, ...);
jdouble CallDoubleMethod(jclass clazz, jmethodID methodID, ...);
void CallVoidMethod(jclass clazz, jmethodID methodID, ...);
```

这个函数与 CallXXXXXMethod 类似，但它使用一个 jvalue 数组来传递参数，而不是可变参数列表，这使得它在参数数量或类型不确定的情况下更加灵活

```cpp
jobject CallObjectMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jboolean CallBooleanMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jbyte CallByteMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jchar CallCharMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jshort CallShortMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jint CallIntMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jlong CallLongMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jfloat CallFloatMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
jdouble CallDoubleMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
void CallVoidMethodA(jclass clazz, jmethodID methodID, const jvalue * args);
```

这个函数与 CallXXXXXMethod 和 CallXXXXXMethodA 类似，但它使用 va_list 可变参数列表，这使得它在参数传递方式上更加灵活，适用于需要动态构建参数列表的场景

```cpp
jobject CallObjectMethodV(jclass clazz, jmethodID methodID, va_list args);
jboolean CallBooleanMethodV(jclass clazz, jmethodID methodID, va_list args);
jbyte CallByteMethodV(jclass clazz, jmethodID methodID, va_list args);
jchar CallCharMethodV(jclass clazz, jmethodID methodID, va_list args);
jshort CallShortMethodV(jclass clazz, jmethodID methodID, va_list args);
jint CallIntMethodV(jclass clazz, jmethodID methodID, va_list args);
jlong CallLongMethodV(jclass clazz, jmethodID methodID, va_list args);
jfloat CallFloatMethodV(jclass clazz, jmethodID methodID, va_list args);
jdouble CallDoubleMethodV(jclass clazz, jmethodID methodID, va_list args);
void CallVoidMethodV(jclass clazz, jmethodID methodID, va_list args);
```

## 在 c++ 中调用 Java 父类的实例方法

在 JNI 中访问方法的步骤:

1. 通过 GetObjectClass 获取 java 对象所属的类
2. 通过 GetMethodID, 根据方法名和方法的签名, 获取类中指定方法的 ID
3. 根据方法的 ID 调用 CallNonvirtualXXXXXXMethod 调用 java 方法(super.xxx)
