# main 函数

main 工作的重点是：创建一个运行环境，为接下来启动一个新的线程创建 JVM 并跳到 Java 主方法做好一切准备工作。

在 main 函数执行的最后一步，程序将启动一个新的线程并将 Java 程序参数传递给它，接下来阻塞自己，并在新线程中继续执行。新线程也可称为为主线程，它的执行入口是 JavaMain。

```c
// --- src/java.base/share/native/launcher/main.c --- //
#include "defines.h"
#include "jli_util.h"
#include "jni.h"

// 通过javaw命令启动的程序
// #ifdef JAVAW

// char **__initenv;

// Windows系统的main函数

// int WINAPI
// WinMain(HINSTANCE inst, HINSTANCE previnst, LPSTR cmdline, int cmdshow)
// {
//     int margc;
//     char** margv;
//     int jargc;
//     char** jargv;
//     const jboolean const_javaw = JNI_TRUE;

//     __initenv = _environ;

// #else /* JAVAW */

// 通过java命令启动的程序
JNIEXPORT int
main(int argc, char **argv)
{
    int margc;
    char** margv;
    int jargc;
    char** jargv;
    const jboolean const_javaw = JNI_FALSE;
// #endif /* JAVAW */
    {
        int i, main_jargc, extra_jargc;
        JLI_List list;

        main_jargc = (sizeof(const_jargs) / sizeof(char *)) > 1
            ? sizeof(const_jargs) / sizeof(char *)
            : 0; // ignore the null terminator index

        extra_jargc = (sizeof(const_extra_jargs) / sizeof(char *)) > 1
            ? sizeof(const_extra_jargs) / sizeof(char *)
            : 0; // ignore the null terminator index

        if (main_jargc > 0 && extra_jargc > 0) { // combine extra java args
            jargc = main_jargc + extra_jargc;
            list = JLI_List_new(jargc + 1);

            for (i = 0 ; i < extra_jargc; i++) {
                JLI_List_add(list, JLI_StringDup(const_extra_jargs[i]));
            }

            for (i = 0 ; i < main_jargc ; i++) {
                JLI_List_add(list, JLI_StringDup(const_jargs[i]));
            }

            // terminate the list
            JLI_List_add(list, NULL);
            jargv = list->elements;
         } else if (extra_jargc > 0) { // should never happen
            fprintf(stderr, "EXTRA_JAVA_ARGS defined without JAVA_ARGS");
            abort();
         } else { // no extra args, business as usual
            jargc = main_jargc;
            jargv = (char **) const_jargs;
         }
    }

    JLI_InitArgProcessing(jargc > 0, const_disable_argfile);

// #ifdef _WIN32
//     {
//         int i = 0;
//         if (getenv(JLDEBUG_ENV_ENTRY) != NULL) {
//             printf("Windows original main args:\n");
//             for (i = 0 ; i < __argc ; i++) {
//                 printf("wwwd_args[%d] = %s\n", i, __argv[i]);
//             }
//         }
//     }
//     JLI_CmdToArgs(GetCommandLine());
//     margc = JLI_GetStdArgc();
//     // add one more to mark the end
//     margv = (char **)JLI_MemAlloc((margc + 1) * (sizeof(char *)));
//     {
//         int i = 0;
//         StdArg *stdargs = JLI_GetStdArgs();
//         for (i = 0 ; i < margc ; i++) {
//             margv[i] = stdargs[i].arg;
//         }
//         margv[i] = NULL;
//     }
// #else /* *NIXES */
    {
        // accommodate the NULL at the end
        JLI_List args = JLI_List_new(argc + 1);
        int i = 0;

        // Add first arg, which is the app name
        JLI_List_add(args, JLI_StringDup(argv[0]));
        // Append JDK_JAVA_OPTIONS
        if (JLI_AddArgsFromEnvVar(args, JDK_JAVA_OPTIONS)) {
            // JLI_SetTraceLauncher is not called yet
            // Show _JAVA_OPTIONS content along with JDK_JAVA_OPTIONS to aid diagnosis
            if (getenv(JLDEBUG_ENV_ENTRY)) {
                char *tmp = getenv("_JAVA_OPTIONS");
                if (NULL != tmp) {
                    JLI_ReportMessage(ARG_INFO_ENVVAR, "_JAVA_OPTIONS", tmp);
                }
            }
        }
        // Iterate the rest of command line
        for (i = 1; i < argc; i++) {
            JLI_List argsInFile = JLI_PreprocessArg(argv[i], JNI_TRUE);
            if (NULL == argsInFile) {
                JLI_List_add(args, JLI_StringDup(argv[i]));
            } else {
                int cnt, idx;
                cnt = argsInFile->size;
                for (idx = 0; idx < cnt; idx++) {
                    JLI_List_add(args, argsInFile->elements[idx]);
                }
                // Shallow free, we reuse the string to avoid copy
                JLI_MemFree(argsInFile->elements);
                JLI_MemFree(argsInFile);
            }
        }
        margc = args->size;
        // add the NULL pointer at argv[argc]
        JLI_List_add(args, NULL);
        margv = args->elements;
    }
// #endif /* WIN32 */
    return JLI_Launch(margc, margv,
                   jargc, (const char**) jargv,
                   0, NULL,
                   VERSION_STRING,
                   DOT_VERSION,
                   (const_progname != NULL) ? const_progname : *margv,
                   (const_launcher != NULL) ? const_launcher : *margv,
                   jargc > 0,
                   const_cpwildcard, const_javaw, 0);
}
```

## JLI_Launch

LoadJavaVM 创建虚拟机。JVMInit 初始化 JVM 并在新线程中继续执行。

```c
// --- src/java.base/share/native/libjli/java.c --- //

JNIEXPORT int JNICALL
JLI_Launch(int argc, char ** argv,              /* main argc, argv */
        int jargc, const char** jargv,          /* java args */
        int appclassc, const char** appclassv,  /* app classpath */
        const char* fullversion,                /* full version defined */
        const char* dotversion,                 /* UNUSED dot version defined */
        const char* pname,                      /* program name */
        const char* lname,                      /* launcher name */
        jboolean javaargs,                      /* JAVA_ARGS */
        jboolean cpwildcard,                    /* classpath wildcard*/
        jboolean javaw,                         /* windows-only javaw */
        jint ergo                               /* unused */
)
{
    int mode = LM_UNKNOWN;
    char *what = NULL;
    char *main_class = NULL;
    int ret;
    InvocationFunctions ifn;
    jlong start = 0, end = 0;
    char jvmpath[MAXPATHLEN];
    char jrepath[MAXPATHLEN];
    char jvmcfg[MAXPATHLEN];

    _fVersion = fullversion;
    _launcher_name = lname;
    _program_name = pname;
    _is_java_args = javaargs;
    _wc_enabled = cpwildcard;

    InitLauncher(javaw);
    DumpState();
    if (JLI_IsTraceLauncher()) {
        int i;
        printf("Java args:\n");
        for (i = 0; i < jargc ; i++) {
            printf("jargv[%d] = %s\n", i, jargv[i]);
        }
        printf("Command line args:\n");
        for (i = 0; i < argc ; i++) {
            printf("argv[%d] = %s\n", i, argv[i]);
        }
        AddOption("-Dsun.java.launcher.diag=true", NULL);
    }

    /*
     * SelectVersion() has several responsibilities:
     *
     *  1) Disallow specification of another JRE.  With 1.9, another
     *     version of the JRE cannot be invoked.
     *  2) Allow for a JRE version to invoke JDK 1.9 or later.  Since
     *     all mJRE directives have been stripped from the request but
     *     the pre 1.9 JRE [ 1.6 thru 1.8 ], it is as if 1.9+ has been
     *     invoked from the command line.
     */
    SelectVersion(argc, argv, &main_class);

    CreateExecutionEnvironment(&argc, &argv,
                               jrepath, sizeof(jrepath),
                               jvmpath, sizeof(jvmpath),
                               jvmcfg,  sizeof(jvmcfg));

    ifn.CreateJavaVM = 0;
    ifn.GetDefaultJavaVMInitArgs = 0;

    if (JLI_IsTraceLauncher()) {
        start = CurrentTimeMicros();
    }

    if (!LoadJavaVM(jvmpath, &ifn)) {
        return(6);
    }

    if (JLI_IsTraceLauncher()) {
        end   = CurrentTimeMicros();
    }

    JLI_TraceLauncher("%ld micro seconds to LoadJavaVM\n", (long)(end-start));

    ++argv;
    --argc;

    if (IsJavaArgs()) {
        /* Preprocess wrapper arguments */
        TranslateApplicationArgs(jargc, jargv, &argc, &argv);
        if (!AddApplicationOptions(appclassc, appclassv)) {
            return(1);
        }
    } else {
        /* Set default CLASSPATH */
        char* cpath = getenv("CLASSPATH");
        if (cpath != NULL) {
            SetClassPath(cpath);
        }
    }

    /* Parse command line options; if the return value of
     * ParseArguments is false, the program should exit.
     */
    if (!ParseArguments(&argc, &argv, &mode, &what, &ret, jrepath)) {
        return(ret);
    }

    /* Override class path if -jar flag was specified */
    if (mode == LM_JAR) {
        SetClassPath(what);     /* Override class path */
    }

    /* set the -Dsun.java.command pseudo property */
    SetJavaCommandLineProp(what, argc, argv);

    /* Set the -Dsun.java.launcher pseudo property */
    SetJavaLauncherProp();

    return JVMInit(&ifn, threadStackSize, argc, argv, mode, what, ret);
}
```

## JVMInit

`.m` ：Xcode 源代码文件。可以包含 Objective-C 和 C 代码。

```c
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

// MacOSX we may continue in the same thread
int
JVMInit(InvocationFunctions* ifn, jlong threadStackSize,
                 int argc, char **argv,
                 int mode, char *what, int ret) {
    if (sameThread) {
        JLI_TraceLauncher("In same thread\n");
        // need to block this thread against the main thread
        // so signals get caught correctly
        __block int rslt = 0;
        NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
        {
            NSBlockOperation *op = [NSBlockOperation blockOperationWithBlock: ^{
                JavaMainArgs args;
                args.argc = argc;
                args.argv = argv;
                args.mode = mode;
                args.what = what;
                args.ifn  = *ifn;
                rslt = JavaMain(&args);
            }];

            /*
             * We cannot use dispatch_sync here, because it blocks the main dispatch queue.
             * Using the main NSRunLoop allows the dispatch queue to run properly once
             * SWT (or whatever toolkit this is needed for) kicks off it's own NSRunLoop
             * and starts running.
             */
            [op performSelectorOnMainThread:@selector(start) withObject:nil waitUntilDone:YES];
        }
        [pool drain];
        return rslt;
    } else {
        return ContinueInNewThread(ifn, threadStackSize, argc, argv, mode, what, ret);
    }
}
```

## ContinueInNewThread

```c
// --- src/java.base/share/native/libjli/java.c --- //

int
ContinueInNewThread(InvocationFunctions* ifn, jlong threadStackSize,
                    int argc, char **argv,
                    int mode, char *what, int ret)
{
    if (threadStackSize == 0) {
        /*
         * If the user hasn't specified a non-zero stack size ask the JVM for its default.
         * A returned 0 means 'use the system default' for a platform, e.g., Windows.
         * Note that HotSpot no longer supports JNI_VERSION_1_1 but it will
         * return its default stack size through the init args structure.
         */
        struct JDK1_1InitArgs args1_1;
        memset((void*)&args1_1, 0, sizeof(args1_1));
        args1_1.version = JNI_VERSION_1_1;
        ifn->GetDefaultJavaVMInitArgs(&args1_1);  /* ignore return value */
        if (args1_1.javaStackSize > 0) {
            threadStackSize = args1_1.javaStackSize;
        }
    }

    { /* Create a new thread to create JVM and invoke main method */
        JavaMainArgs args;
        int rslt;

        args.argc = argc;
        args.argv = argv;
        args.mode = mode;
        args.what = what;
        args.ifn = *ifn;

        rslt = CallJavaMainInNewThread(threadStackSize, (void*)&args);
        /* If the caller has deemed there is an error we
         * simply return that, otherwise we return the value of
         * the callee
         */
        return (ret != 0) ? ret : rslt;
    }
}
```

## CallJavaMainInNewThread

```c
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

/*
 * Block current thread and continue execution in a new thread.
 */
int
CallJavaMainInNewThread(jlong stack_size, void* args) {
    int rslt;
    pthread_t tid;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    if (stack_size > 0) {
        pthread_attr_setstacksize(&attr, adjustStackSize(stack_size));
    }
    pthread_attr_setguardsize(&attr, 0); // no pthread guard page on java threads

    if (pthread_create(&tid, &attr, ThreadJavaMain, args) == 0) {
        void* tmp;
        pthread_join(tid, &tmp);
        rslt = (int)(intptr_t)tmp;
    } else {
       /*
        * Continue execution in current thread if for some reason (e.g. out of
        * memory/LWP)  a new thread can't be created. This will likely fail
        * later in JavaMain as JNI_CreateJavaVM needs to create quite a
        * few new threads, anyway, just give it a try..
        */
        rslt = JavaMain(args);
    }

    pthread_attr_destroy(&attr);
    return rslt;
}

static void* ThreadJavaMain(void* args) {
    return (void*)(intptr_t)JavaMain(args);
}
```
