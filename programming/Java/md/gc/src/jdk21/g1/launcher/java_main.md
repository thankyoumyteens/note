# JavaMain

一般来说，主线程(JavaMain)将伴随应用程序的整个生命周期。

其中有几个重要的局部变量:

1. `InvocationFunctions ifn`
2. `JavaVM *vm`
3. `JNIEnv *env`

## InvocationFunctions

```c
// --- src/java.base/share/native/libjli/java.h --- //

typedef struct {
    CreateJavaVM_t CreateJavaVM;
    GetDefaultJavaVMInitArgs_t GetDefaultJavaVMInitArgs;
    GetCreatedJavaVMs_t GetCreatedJavaVMs;
} InvocationFunctions;
```

## JavaVM

```cpp
// --- build/macosx-aarch64-serverANDclient-slowdebug/support/modules_include/java.base/jni.h --- //

typedef JavaVM_ JavaVM;

struct JavaVM_ {
    const struct JNIInvokeInterface_ *functions;

    jint DestroyJavaVM() {
        return functions->DestroyJavaVM(this);
    }
    jint AttachCurrentThread(void **penv, void *args) {
        return functions->AttachCurrentThread(this, penv, args);
    }
    jint DetachCurrentThread() {
        return functions->DetachCurrentThread(this);
    }

    jint GetEnv(void **penv, jint version) {
        return functions->GetEnv(this, penv, version);
    }
    jint AttachCurrentThreadAsDaemon(void **penv, void *args) {
        return functions->AttachCurrentThreadAsDaemon(this, penv, args);
    }
};
```

## JNIEnv

JNIEnv 中包含了大量的 JNI 函数以供 JVM 和用户的 JNI 代码调用。

```cpp
// --- build/macosx-aarch64-serverANDclient-slowdebug/support/modules_include/java.base/jni.h --- //

typedef JNIEnv_ JNIEnv;

struct JNIEnv_ {
    const struct JNINativeInterface_ *functions;

    // ...
    jclass GetObjectClass(jobject obj) {
        return functions->GetObjectClass(this,obj);
    }

    // ...

    jmethodID GetMethodID(jclass clazz, const char *name,
                          const char *sig) {
        return functions->GetMethodID(this,clazz,name,sig);
    }
    // ...
};
```

## JavaMain 的执行流程

```c
// --- src/java.base/share/native/libjli/java.c --- //

int
JavaMain(void* _args)
{
    JavaMainArgs *args = (JavaMainArgs *)_args;
    int argc = args->argc;
    char **argv = args->argv;
    int mode = args->mode;
    char *what = args->what;
    InvocationFunctions ifn = args->ifn;

    JavaVM *vm = 0;
    JNIEnv *env = 0;
    jclass mainClass = NULL;
    jclass appClass = NULL; // actual application class being launched
    jobjectArray mainArgs;
    jmethodID mainID;
    jmethodID constructor;
    jobject mainObject;
    int ret = 0;
    jlong start = 0, end = 0;

    RegisterThread();

    /* Initialize the virtual machine */
    start = CurrentTimeMicros();
    if (!InitializeJVM(&vm, &env, &ifn)) {
        JLI_ReportErrorMessage(JVM_ERROR1);
        exit(1);
    }

    if (showSettings != NULL) {
        ShowSettings(env, showSettings);
        CHECK_EXCEPTION_LEAVE(1);
    }

    // show resolved modules and continue
    if (showResolvedModules) {
        ShowResolvedModules(env);
        CHECK_EXCEPTION_LEAVE(1);
    }

    // list observable modules, then exit
    if (listModules) {
        ListModules(env);
        CHECK_EXCEPTION_LEAVE(1);
        LEAVE();
    }

    // describe a module, then exit
    if (describeModule != NULL) {
        DescribeModule(env, describeModule);
        CHECK_EXCEPTION_LEAVE(1);
        LEAVE();
    }

    if (printVersion || showVersion) {
        PrintJavaVersion(env);
        CHECK_EXCEPTION_LEAVE(0);
        if (printVersion) {
            LEAVE();
        }
    }

    // modules have been validated at startup so exit
    if (validateModules) {
        LEAVE();
    }

    /* If the user specified neither a class name nor a JAR file */
    if (printXUsage || printUsage || what == 0 || mode == LM_UNKNOWN) {
        PrintUsage(env, printXUsage);
        CHECK_EXCEPTION_LEAVE(1);
        LEAVE();
    }

    FreeKnownVMs(); /* after last possible PrintUsage */

    if (JLI_IsTraceLauncher()) {
        end = CurrentTimeMicros();
        JLI_TraceLauncher("%ld micro seconds to InitializeJVM\n", (long)(end-start));
    }

    /* At this stage, argc/argv have the application's arguments */
    if (JLI_IsTraceLauncher()){
        int i;
        printf("%s is '%s'\n", launchModeNames[mode], what);
        printf("App's argc is %d\n", argc);
        for (i=0; i < argc; i++) {
            printf("    argv[%2d] = '%s'\n", i, argv[i]);
        }
    }

    ret = 1;

    /*
     * Get the application's main class. It also checks if the main
     * method exists.
     *
     * See bugid 5030265.  The Main-Class name has already been parsed
     * from the manifest, but not parsed properly for UTF-8 support.
     * Hence the code here ignores the value previously extracted and
     * uses the pre-existing code to reextract the value.  This is
     * possibly an end of release cycle expedient.  However, it has
     * also been discovered that passing some character sets through
     * the environment has "strange" behavior on some variants of
     * Windows.  Hence, maybe the manifest parsing code local to the
     * launcher should never be enhanced.
     *
     * Hence, future work should either:
     *     1)   Correct the local parsing code and verify that the
     *          Main-Class attribute gets properly passed through
     *          all environments,
     *     2)   Remove the vestages of maintaining main_class through
     *          the environment (and remove these comments).
     *
     * This method also correctly handles launching existing JavaFX
     * applications that may or may not have a Main-Class manifest entry.
     */
    mainClass = LoadMainClass(env, mode, what);
    CHECK_EXCEPTION_NULL_LEAVE(mainClass);
    /*
     * In some cases when launching an application that needs a helper, e.g., a
     * JavaFX application with no main method, the mainClass will not be the
     * applications own main class but rather a helper class. To keep things
     * consistent in the UI we need to track and report the application main class.
     */
    appClass = GetApplicationClass(env);
    NULL_CHECK_RETURN_VALUE(appClass, -1);

    /* Build platform specific argument array */
    mainArgs = CreateApplicationArgs(env, argv, argc);
    CHECK_EXCEPTION_NULL_LEAVE(mainArgs);

    if (dryRun) {
        ret = 0;
        LEAVE();
    }

    /*
     * PostJVMInit uses the class name as the application name for GUI purposes,
     * for example, on OSX this sets the application name in the menu bar for
     * both SWT and JavaFX. So we'll pass the actual application class here
     * instead of mainClass as that may be a launcher or helper class instead
     * of the application class.
     */
    PostJVMInit(env, appClass, vm);
    CHECK_EXCEPTION_LEAVE(1);

    /*
     * The LoadMainClass not only loads the main class, it will also ensure
     * that the main method's signature is correct, therefore further checking
     * is not required. The main method is invoked here so that extraneous java
     * stacks are not in the application stack trace.
     */
#define MAIN_WITHOUT_ARGS 1
#define MAIN_NONSTATIC 2

    jclass helperClass = GetLauncherHelperClass(env);
    jmethodID getMainType = (*env)->GetStaticMethodID(env, helperClass,
                                                      "getMainType",
                                                      "()I");
    CHECK_EXCEPTION_NULL_LEAVE(getMainType);
    int mainType = (*env)->CallStaticIntMethod(env, helperClass, getMainType);
    CHECK_EXCEPTION_LEAVE(mainType);

    switch (mainType) {
    case 0: {
        mainID = (*env)->GetStaticMethodID(env, mainClass, "main",
                                           "([Ljava/lang/String;)V");
        CHECK_EXCEPTION_NULL_LEAVE(mainID);
        (*env)->CallStaticVoidMethod(env, mainClass, mainID, mainArgs);
        break;
        }
    case MAIN_WITHOUT_ARGS: {
        mainID = (*env)->GetStaticMethodID(env, mainClass, "main",
                                           "()V");
        CHECK_EXCEPTION_NULL_LEAVE(mainID);
        (*env)->CallStaticVoidMethod(env, mainClass, mainID);
        break;
        }
    case MAIN_NONSTATIC: {
        constructor = (*env)->GetMethodID(env, mainClass, "<init>", "()V");
        CHECK_EXCEPTION_NULL_LEAVE(constructor);
        mainObject = (*env)->NewObject(env, mainClass, constructor);
        CHECK_EXCEPTION_NULL_LEAVE(mainObject);
        mainID = (*env)->GetMethodID(env, mainClass, "main",
                                     "([Ljava/lang/String;)V");
        CHECK_EXCEPTION_NULL_LEAVE(mainID);
        (*env)->CallVoidMethod(env, mainObject, mainID, mainArgs);
        break;
        }
    case MAIN_NONSTATIC | MAIN_WITHOUT_ARGS: {
        constructor = (*env)->GetMethodID(env, mainClass, "<init>", "()V");
        CHECK_EXCEPTION_NULL_LEAVE(constructor);
        mainObject = (*env)->NewObject(env, mainClass, constructor);
        CHECK_EXCEPTION_NULL_LEAVE(mainObject);
        mainID = (*env)->GetMethodID(env, mainClass, "main",
                                     "()V");
        CHECK_EXCEPTION_NULL_LEAVE(mainID);
        (*env)->CallVoidMethod(env, mainObject, mainID);
        break;
        }
    }

    /*
     * The launcher's exit code (in the absence of calls to
     * System.exit) will be non-zero if main threw an exception.
     */
    ret = (*env)->ExceptionOccurred(env) == NULL ? 0 : 1;

    LEAVE();
}
```
