# JNI 对象字段操作

在 JNI 中访问对象字段的步骤:

1. 通过 GetObjectClass 获取 java 对象所属的类
2. 通过 GetFieldID 获取类中指定字段的 FieldID
3. 使用 FieldID 调用 GetObjectField 等方法获取字段值
4. 使用 FieldID 调用 SetObjectField 等方法修改字段值

```cpp
jclass GetObjectClass(JNIEnv *env, jobject obj);
// name: 字段名, sig: 字段描述符
jfieldID GetFieldID(JNIEnv *env, jclass clazz, const char *name, const char *sig);

// 字段取值
jobject GetObjectField(JNIEnv *env, jobject obj, jfieldID fieldID);
jboolean GetBooleanField(JNIEnv *env, jobject obj, jfieldID fieldID);
jbyte GetByteField(JNIEnv *env, jobject obj, jfieldID fieldID);
jchar GetCharField(JNIEnv *env, jobject obj, jfieldID fieldID);
jshort GetShortField(JNIEnv *env, jobject obj, jfieldID fieldID);
jint GetIntField(JNIEnv *env, jobject obj, jfieldID fieldID);
jlong GetLongField(JNIEnv *env, jobject obj, jfieldID fieldID);
jfloat GetFloatField(JNIEnv *env, jobject obj, jfieldID fieldID);
jdouble GetDoubleField(JNIEnv *env, jobject obj, jfieldID fieldID);

// 字段赋值
void SetObjectField(JNIEnv *env, jobject obj, jfieldID fieldID, jobject val);
void SetBooleanField(JNIEnv *env, jobject obj, jfieldID fieldID, jboolean val);
void SetByteField(JNIEnv *env, jobject obj, jfieldID fieldID, jbyte val);
void SetCharField(JNIEnv *env, jobject obj, jfieldID fieldID, jchar val);
void SetShortField(JNIEnv *env, jobject obj, jfieldID fieldID, jshort val);
void SetIntField(JNIEnv *env, jobject obj, jfieldID fieldID, jint val);
void SetLongField(JNIEnv *env, jobject obj, jfieldID fieldID, jlong val);
void SetFloatField(JNIEnv *env, jobject obj, jfieldID fieldID, jfloat val);
void SetDoubleField(JNIEnv *env, jobject obj, jfieldID fieldID, jdouble val);
```
