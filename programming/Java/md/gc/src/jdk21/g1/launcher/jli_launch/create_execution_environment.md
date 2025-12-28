# 构建一个可以启动 JVM 的运行环境

```cpp
// --- src/java.base/share/native/libjli/java.h --- //

/**
 * 根据命令行、环境、系统情况，构建好一个“可以启动 JVM 的运行环境”，
 * 并把关键路径信息（JRE 目录、JVM 动态库路径、配置文件路径）返回给调用者
 *
 * 不同平台会各自实现这个函数
 *
 * MacOS 系统下, 会使用: src/java.base/macosx/native/libjli/java_md_macosx.m
 *
 * @param argc 原始的命令行参数个数
 * @param argv 指向原始的命令行参数数组
 * @param jrepath 函数返回的“可访问的 JRE 路径”会写到这里
 * @param so_jrepath jrepath 缓冲区的长度（防止写溢出）
 * @param jvmpath 函数返回的“可访问的 JVM 库路径”会写到这里
 * @param so_jvmpath jvmpath 缓冲区的长度
 * @param jvmcfg 缓冲区，用来返回 jvm.cfg 配置文件的路径
 * @param so_jvmcfg jvmcfg 缓冲区的长度
 */
void CreateExecutionEnvironment(int *argc, char ***argv,
                                char *jrepath, jint so_jrepath,
                                char *jvmpath, jint so_jvmpath,
                                char *jvmcfg,  jint so_jvmcfg);
```

## MacOS 实现

```cpp
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

void
CreateExecutionEnvironment(int *pargc, char ***pargv,
                           char jrepath[], jint so_jrepath,
                           char jvmpath[], jint so_jvmpath,
                           char jvmcfg[],  jint so_jvmcfg) {
    // 记录当前可执行文件的名字
    SetExecname(*pargv);

    // 将来用来保存 JVM 类型字符串（比如 "client", "server", 甚至是错误标记 "ERROR"）
    char * jvmtype    = NULL;
    int  argc         = *pargc;
    char **argv       = *pargv;

    // 找到要使用的 JRE
    if (!GetJREPath(jrepath, so_jrepath, JNI_FALSE) ) {
        JLI_ReportErrorMessage(JRE_ERROR1);
        exit(2);
    }
    // 拼出 jvm.cfg 文件的路径
    JLI_Snprintf(jvmcfg, so_jvmcfg, "%s%slib%sjvm.cfg",
                 jrepath, FILESEP, FILESEP);
    // 解析 jvm.cfg，把里面列出的可用 VM 类型（client、server 等）加载到内部结构中
    if (ReadKnownVMs(jvmcfg, JNI_FALSE) < 1) {
        JLI_ReportErrorMessage(CFG_ERROR7);
        exit(1);
    }

    // 先把 jvmpath 清空，表示目前还没有选定 JVM 路径
    jvmpath[0] = '\0';
    // 分析命令行，决定用哪个 JVM 类型
    jvmtype = CheckJvmType(pargc, pargv, JNI_FALSE);
    // 如果命令行中指定了无效/不支持的 VM 类型，CheckJvmType 可能返回 "ERROR"
    if (JLI_StrCmp(jvmtype, "ERROR") == 0) {
        JLI_ReportErrorMessage(CFG_ERROR9);
        exit(4);
    }

    // 根据 jrepath + jvmtype 找到真正的 JVM 动态库
    if (!GetJVMPath(jrepath, jvmtype, jvmpath, so_jvmpath)) {
        JLI_ReportErrorMessage(CFG_ERROR8, jvmtype, jvmpath);
        exit(4);
    }

    // macOS 特有：启动 Cocoa 事件循环
    MacOSXStartup(argc, argv);

    return;
}
```
