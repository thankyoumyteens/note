# JNI 数据类型

JNI 类型和 Java 基本类型的对应:

- jint -> int
- jbyte -> byte
- jshort -> short
- jlong -> long
- jfloat -> float
- jdouble -> double
- jchar -> char
- jboolean -> boolean

JNI 类型和 Java 引用类型的对应:

- jobject -> java.lang.Object
- jclass -> java.lang.Class
- jstring -> java.lang.String
- jthrowable -> java.lang.Throwable
- jarray -> Java 数组

Java 数组分为 8 个基本类型数组和 1 个对象数组: jintArray, jbyteArray, jshortArray, jlongArray, jfloatArray, jdoubleArray, jcharArray,  jbooleanArray 和 jobjectArray。
