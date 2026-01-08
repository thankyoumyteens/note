# 加载 JVM 动态库

```cpp
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

/**
 * 根据 jvmpath 动态加载 JVM 动态库，
 * 然后把 JNI_CreateJavaVM 等函数地址保存起来，后面会用它们去真正创建 JVM
 *
 * @param jvmpath libjvm 的路径，比如：
 *                - Linux：.../lib/server/libjvm.so
 *                - macOS：.../lib/server/libjvm.dylib
 *                - Windows 上对应会是 jvm.dll
 * @param ifn 一个结构体指针，里边会存三个函数指针：
 *            - CreateJavaVM
 *            - GetDefaultJavaVMInitArgs
 *            - GetCreatedJavaVMs
 */
jboolean
LoadJavaVM(const char *jvmpath, InvocationFunctions *ifn)
{
    void *libjvm;

    JLI_TraceLauncher("JVM path is %s\n", jvmpath);

    // 使用 dlopen 加载 JVM 动态库
#ifndef STATIC_BUILD // 注意这里是 ifndef
    // 非静态构建（正常情况）
    // 按给定路径打开共享库，返回一个 handle
    // RTLD_NOW：立刻解析所有未解析的符号
    // RTLD_GLOBAL：将这个库中的符号放入全局符号表，后续加载的库可以看到这些符号
    //              因为 libjvm 里可能还会被其他动态库依赖（比如 AWT、JFR 等）
    libjvm = dlopen(jvmpath, RTLD_NOW + RTLD_GLOBAL);
#else
    // 静态构建
    // NULL：表示“当前进程本身的可执行文件”, 对应静态链接场景：libjvm 的代码直接链接进了可执行文件，
    //       这时不需要单独的 libjvm.so，只在进程自身里找符号即可。
    // RTLD_FIRST：优先从该 handle（这里是 main 程序）里解析符号，而不是从全局其它共享库中
    libjvm = dlopen(NULL, RTLD_FIRST);
#endif
    if (libjvm == NULL) {
        // dlopen 失败
        JLI_ReportErrorMessage(DLL_ERROR1, __LINE__);
        JLI_ReportErrorMessage(DLL_ERROR2, jvmpath, dlerror());
        return JNI_FALSE;
    }

    // 从 libjvm 中查三大 JNI 函数

    // 在 libjvm 这个库里找符号名 "JNI_CreateJavaVM"
    // 找到后返回其地址，强转成 CreateJavaVM_t 函数指针类型
    // 这个函数后面就是用来真正创建 JVM
    ifn->CreateJavaVM = (CreateJavaVM_t)
        dlsym(libjvm, "JNI_CreateJavaVM");
    if (ifn->CreateJavaVM == NULL) {
        // 没找到
        JLI_ReportErrorMessage(DLL_ERROR2, jvmpath, dlerror());
        return JNI_FALSE;
    }

    // 这个函数用于在创建 JVM 前获取“默认初始化参数”（内存、class path 等一些默认设置）
    // Launcher 通常会先调用这个函数，然后在返回的结构上做一些修改（比如添加 -Xmx、-D 系列参数），
    // 再传给 JNI_CreateJavaVM
    ifn->GetDefaultJavaVMInitArgs = (GetDefaultJavaVMInitArgs_t)
        dlsym(libjvm, "JNI_GetDefaultJavaVMInitArgs");
    if (ifn->GetDefaultJavaVMInitArgs == NULL) {
        JLI_ReportErrorMessage(DLL_ERROR2, jvmpath, dlerror());
        return JNI_FALSE;
    }

    // 这个函数用于获取当前进程中已经创建的 JVM 实例
    // 在嵌入式场景中用得多，比如 C 程序已经启动过 JVM，再次进来要复用已有的 VM，而不是重新创建
    ifn->GetCreatedJavaVMs = (GetCreatedJavaVMs_t)
    dlsym(libjvm, "JNI_GetCreatedJavaVMs");
    if (ifn->GetCreatedJavaVMs == NULL) {
        JLI_ReportErrorMessage(DLL_ERROR2, jvmpath, dlerror());
        return JNI_FALSE;
    }

    return JNI_TRUE;
}
```
