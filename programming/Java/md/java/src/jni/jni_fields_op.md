# JNI 操作对象的字段

在 JNI 中访问对象字段的步骤:

1. 通过 GetObjectClass 获取 java 对象所属的类
2. 通过 GetFieldID 获取类中指定字段的 FieldID
3. 使用 FieldID 调用 GetObjectField 等方法获取字段值
4. 使用 FieldID 调用 SetObjectField 等方法修改字段值

```cpp
jclass GetObjectClass(jobject obj);
// name: 字段名, sig: 字段描述符
jfieldID GetFieldID(jclass clazz, const char *name, const char *sig);
```

## 字段取值

```cpp
jobject GetObjectField(jobject obj, jfieldID fieldID);
jboolean GetBooleanField(jobject obj, jfieldID fieldID);
jbyte GetByteField(jobject obj, jfieldID fieldID);
jchar GetCharField(jobject obj, jfieldID fieldID);
jshort GetShortField(jobject obj, jfieldID fieldID);
jint GetIntField(jobject obj, jfieldID fieldID);
jlong GetLongField(jobject obj, jfieldID fieldID);
jfloat GetFloatField(jobject obj, jfieldID fieldID);
jdouble GetDoubleField(jobject obj, jfieldID fieldID);
```

## 字段赋值

```cpp
void SetObjectField(jobject obj, jfieldID fieldID, jobject val);
void SetBooleanField(jobject obj, jfieldID fieldID, jboolean val);
void SetByteField(jobject obj, jfieldID fieldID, jbyte val);
void SetCharField(jobject obj, jfieldID fieldID, jchar val);
void SetShortField(jobject obj, jfieldID fieldID, jshort val);
void SetIntField(jobject obj, jfieldID fieldID, jint val);
void SetLongField(jobject obj, jfieldID fieldID, jlong val);
void SetFloatField(jobject obj, jfieldID fieldID, jfloat val);
void SetDoubleField(jobject obj, jfieldID fieldID, jdouble val);
```
