# main 函数

该函数是 Java 启动器的主入口点，负责准备和启动 Java 虚拟机。通过在编译时传入不同的编译器参数，可以编译出不同的 JDK 工具, 如 java, javac, jinfo, jmap 等, 它们共用同一个 main 函数源码。

```c
// --- src/java.base/share/native/launcher/main.c --- //

/**
 * main 函数
 * JNIEXPORT 宏标记此函数为 JNI 导出函数
 *
 * @param argc 命令行参数个数(包含程序名)
 * @param argv 命令行参数数组(argv[0]为程序名)
 * @return 0 成功, 非零失败
 */
JNIEXPORT int
main(int argc, char **argv) {
    // 最终传递给 JLI_Launch 的参数个数
    int margc;
    // 最终传递给 JLI_Launch 的参数数组
    char **margv;
    // JDK 内置工具专用参数的个数
    int jargc;
    // JDK 内置工具专用参数的参数数组
    char **jargv;
    // 标记是否以 javaw 方式运行(Windows 平台专属)
    const jboolean const_javaw = JNI_FALSE;

    // 处理启动JDK内置工具(如jinfo, jmap等)时的参数
    {
        // 省略
    }

    // 初始化参数处理系统，设置是否禁用文件参数处理
    // const_disable_argfile 的值由编译时指定的 ENABLE_ARG_FILES 宏决定
    JLI_InitArgProcessing(jargc > 0, const_disable_argfile);

    // 处理命令行参数和环境变量
    {
        // 创建参数列表，大小为命令行参数数量+1(列表的最后一项需要存放一个终止符)
        JLI_List args = JLI_List_new(argc + 1);
        int i = 0;

        // 添加第一个参数，即程序名称
        JLI_List_add(args, JLI_StringDup(argv[0]));

        // 从环境变量 JDK_JAVA_OPTIONS 中添加参数
        // 如果不是 java 命令启动，则不在这里处理环境变量参数
        if (JLI_AddArgsFromEnvVar(args, JDK_JAVA_OPTIONS)) {
            // JLI_SetTraceLauncher 尚未调用
            // 如果启用了调试，同时显示 _JAVA_OPTIONS 内容以帮助诊断
            if (getenv(JLDEBUG_ENV_ENTRY)) {
                char *tmp = getenv("_JAVA_OPTIONS");
                if (NULL != tmp) {
                    JLI_ReportMessage(ARG_INFO_ENVVAR, "_JAVA_OPTIONS", tmp);
                }
            }
        }

        // 处理剩余的命令行参数
        for (i = 1; i < argc; i++) {
            // 预处理参数
            JLI_List argsInFile = JLI_PreprocessArg(argv[i], JNI_TRUE);
            if (NULL == argsInFile) {
                // 不是文件参数，直接把当前参数添加到args列表
                JLI_List_add(args, JLI_StringDup(argv[i]));
            } else {
                // 是文件参数，添加文件中的所有参数
                int cnt, idx;
                cnt = argsInFile->size;
                for (idx = 0; idx < cnt; idx++) {
                    JLI_List_add(args, argsInFile->elements[idx]);
                }
                // 浅释放，重用字符串以避免复制
                JLI_MemFree(argsInFile->elements);
                JLI_MemFree(argsInFile);
            }
        }

        // 计算最终的参数数量
        margc = args->size;
        // 在参数数组末尾添加空指针作为终止符
        JLI_List_add(args, NULL);
        margv = args->elements;
    }

    /*
     * 调用 JLI_Launch 函数启动 Java 应用程序
     *
     * 参数说明:
     *   margc, margv: 合并后的命令行参数
     *   jargc, jargv: JDK 内置工具专用参数
     *   0, NULL: 类路径参数
     *   VERSION_STRING: Java 版本号字符串
     *   DOT_VERSION: 点分版本号
     *   程序名称
     *   启动器名称
     *   jargc > 0: 是否有 JDK 内置工具专用参数
     *   const_cpwildcard: 是否启用类路径(classpath)通配符功能
     *   const_javaw: 是否以 javaw 模式运行(Windows系统专属)
     *   0: 没用到
     */
    return JLI_Launch(margc, margv,
                      jargc, (const char **) jargv,
                      0, NULL,
                      VERSION_STRING,
                      DOT_VERSION,
                      (const_progname != NULL) ? const_progname : *margv,
                      (const_launcher != NULL) ? const_launcher : *margv,
                      jargc > 0,
                      const_cpwildcard, const_javaw, 0);
}
```
