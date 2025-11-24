# InitLauncher 函数

该函数用于初始化 Java 应用程序启动器，设置启动器调试功能的开关。如果开启了启动器调试功能，则会在运行时打印相关的调试信息、记录启动器运行耗时等。

```cpp
// --- src/java.base/unix/native/libjli/java_md_common.c --- //

/**
 * 该函数用于初始化Java应用程序启动器，设置启动器的调试功能
 *
 * @param javaw 是否为 Windows GUI 应用程序(没用到)
 */
void
InitLauncher(jboolean javaw) {
    JLI_SetTraceLauncher();
}

// --- src/java.base/share/native/libjli/jli_util.c --- //

/**
 * 设置启动器调试功能的开关
 *
 * 该函数会检查环境变量 JLDEBUG_ENV_ENTRY 是否被设置，
 * 如果设置了则启用启动器的调试功能
 */
JNIEXPORT void JNICALL
JLI_SetTraceLauncher() {
    if (getenv(JLDEBUG_ENV_ENTRY) != 0) {
        _launcher_debug = JNI_TRUE;
        // 打印启动器调试功能已启用的提示信息
        JLI_TraceLauncher("----%s----\n", JLDEBUG_ENV_ENTRY);
    }
}
```
