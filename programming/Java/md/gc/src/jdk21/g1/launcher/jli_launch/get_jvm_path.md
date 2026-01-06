# 找到真正的 JVM 动态库

```cpp
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

/**
 * 根据 JRE 路径和 JVM 类型，拼出具体 JVM 动态库的绝对路径，并检查这个文件是否存在
 *
 * @param jrepath JRE 根目录，比如 /usr/lib/jvm/java-8-jre
 * @param jvmtype JVM 类型，比如 "client"、"server"，也可能是一个自定义路径
 * @param jvmpath 输出缓冲区，用来存最终生成的 JVM 动态库路径
 * @param jvmpathsize jvmpath 的大小，避免溢出
 */
static jboolean
GetJVMPath(const char *jrepath, const char *jvmtype,
           char *jvmpath, jint jvmpathsize)
{
    struct stat s;

    if (JLI_StrChr(jvmtype, '/')) {
        // jvmtype 中包含 '/'：说明调用者传的不是一个简单类型名，而是一个目录路径
        // 例如: /opt/custom-jvm
        // 那就直接拼：<jvmtype>/<JVM_DLL>
        // 结果：/opt/custom-jvm/libjvm.dylib
        JLI_Snprintf(jvmpath, jvmpathsize, "%s/" JVM_DLL, jvmtype);
    } else {
        // jvmtype 不包含 '/'：这时候把 jvmtype 当成类似 "client"、"server" 这样的“类型名”
        // 标准布局：<jrepath>/lib/<jvmtype>/<JVM_DLL>
        // 比如：
        // - jrepath = /usr/lib/jvm/java-8-jre
        // - jvmtype = server
        // 则路径为：/usr/lib/jvm/java-8-jre/lib/server/libjvm.dylib
        JLI_Snprintf(jvmpath, jvmpathsize, "%s/lib/%s/" JVM_DLL, jrepath, jvmtype);
        // 注意: macOS 客户端库只支持 i386，所以 64 位 client 实际也会转到 server 库加载，
        // 但这个逻辑一般是在别处选择 jvmtype 时处理，这里只是“按既定类型拼路径”。
    }

    JLI_TraceLauncher("Does `%s' exist ... ", jvmpath);

#ifdef STATIC_BUILD
    // 如果是静态构建的 VM（把 JVM 静态链接进可执行文件），那就不用真正去找动态库文件，这里直接返回 JNI_TRUE
    // 在静态构建模式下，这个函数只是走个形式，路径是否有效没关系
    return JNI_TRUE;
#else
    // 非静态构建的情况：用 stat 检查文件是否存在
    if (stat(jvmpath, &s) == 0) {
        JLI_TraceLauncher("yes.\n");
        return JNI_TRUE;
    } else {
        JLI_TraceLauncher("no.\n");
        return JNI_FALSE;
    }
#endif
}
```
