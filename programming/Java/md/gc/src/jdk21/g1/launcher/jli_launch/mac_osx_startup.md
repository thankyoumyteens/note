# 启动 Cocoa 事件循环

```cpp
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

static int (*main_fptr)(int argc, char **argv) = NULL;

/**
 * 这是 pthread_create 要求的线程入口函数形式：void* (*)(void*)
 * arg 是从 pthread_create 传进来的指针，这里实际上传的是一个 struct NSAppArgs*，里面装着 argc 和 argv
 *
 */
static void *apple_main (void *arg)
{
    // 初始化 main_fptr：找到真正的 main 函数
    if (main_fptr == NULL) {
        // 如果还没初始化，就去“找到”真正的 main
#ifdef STATIC_BUILD
        // 静态链接构建时：
        // 直接引用同一个进程里的 main 函数，把它的地址赋给 main_fptr
        // 也就是说，“真正的入口”就是当前程序的 main
        extern int main(int argc, char **argv);
        main_fptr = &main;
#else
        // 普通动态构建时：
        // 使用 dlsym 在默认符号表里查找名为 "main" 的符号(就是 src/java.base/share/native/launcher/main.c 里的 main 函数)
        // 找到后把这个地址当作函数指针赋给 main_fptr
        // 这样做可以在动态加载/不同模块里找到入口
        main_fptr = (int (*)())dlsym(RTLD_DEFAULT, "main");
#endif
        // 如果最终 main_fptr 还是 NULL，说明没找到 main 符号
        if (main_fptr == NULL) {
            JLI_ReportErrorMessageSys("error locating main entrypoint\n");
            exit(1);
        }
    }

    // 把 void* arg 强转回 struct NSAppArgs*
    // 这个 args 是在 MacOSXStartup 函数里构造的
    struct NSAppArgs *args = (struct NSAppArgs *) arg;
    // 在新线程里“再跑一次 main()”并退出
    // 调用 main_fptr(args->argc, args->argv)，也就是相当于在这个新线程里执行：main(args->argc, args->argv);
    // main_fptr 返回一个 int，通常是进程的退出码
    // 然后立刻调用 exit(...)，用这个返回值作为进程退出状态结束整个进程
    exit(main_fptr(args->argc, args->argv));
}

// 一个什么都不干的定时器回调函数
static void dummyTimer(CFRunLoopTimerRef timer, void *info) {}

static void ParkEventLoop() {
    // 创建一个“极远将来才触发”的定时器
    // - 1.0e20：这是一个极其巨大的时间
    // - 0.0：只触发一次（但基本等于永远不会触发）
    // - dummyTimer：一个啥也不做的函数
    // 由于 Core Foundation 的 RunLoop 要有一个“事件源”（source/timer），否则有些情况下不会正确进入等待
    // 于是搞了这么一个“几乎永远不会触发”的 timer，只是满足 RunLoop 的结构要求
    CFRunLoopTimerRef t = CFRunLoopTimerCreate(kCFAllocatorDefault, 1.0e20, 0.0, 0, 0, dummyTimer, NULL);
    // CFRunLoopGetCurrent 拿到当前线程的 RunLoop
    // CFRunLoopAddTimer 把这个 timer 加到默认模式下
    CFRunLoopAddTimer(CFRunLoopGetCurrent(), t, kCFRunLoopDefaultMode);
    // RunLoop 已经持有了 timer 的引用，这里可以把我们自己的引用释放掉，防泄露
    CFRelease(t);

    // 让这个线程永远停在 GUI RunLoop 里，直到整个 RunLoop 被标记成结束
    int32_t result;
    do {
        result = CFRunLoopRunInMode(kCFRunLoopDefaultMode, 1.0e20, false);
    } while (result != kCFRunLoopRunFinished);
}

/**
 * 在 macOS 上，图形界面的事件循环（Cocoa 的主事件循环）必须跑在进程的第一个线程上，也就是通常的 main 线程。
 * 但 Java 想在这个进程里再跑自己的 main(String[] args)。所以这里做的事情是：
 * 1. 把真正跑 Java 自己的 main() 方法的工作丢到一个新线程里去
 * 2. 把原始的 main 线程“空出来”，专门用来跑 Cocoa 的 GUI 事件循环
 */
static void MacOSXStartup(int argc, char *argv[]) {
    // 防止重复启动
    // started 是一个静态局部变量，只在这个函数第一次调用时为 false
    // 如果已经启动过一次，再次调用就直接 return，防止重复创建那个“Java 主线程”
    static jboolean started = false;
    if (started) {
        return;
    }
    started = true;

    // 准备传给新线程的参数
    struct NSAppArgs args;
    args.argc = argc;
    args.argv = argv;

    pthread_t main_thr;
    // 创建新的“主线程”
    // - main_thr：线程句柄
    // - NULL：线程属性使用默认
    // - apple_main：线程函数入口，相当于这个新线程从 apple_main(&args) 开始执行
    // - args：传给 apple_main 的参数
    // 在新的线程中, apple_main 会重新执行一遍 src/java.base/share/native/launcher/main.c 里的 main 函数
    // 当重新执行的 main 函数再次走到这个 MacOSXStartup 函数时, started 的值已经是 true 了
    // 所以不会再走到这里, 而是直接去启动 JVM
    if (pthread_create(&main_thr, NULL, &apple_main, &args) != 0) {
        JLI_ReportErrorMessageSys("Could not create main thread: %s\n", strerror(errno));
        exit(1);
    }
    // 把这个新线程设置为“分离线程”
    // 分离线程的特点：
    // - 它结束时，系统会自动回收其资源
    // - 主线程不需要、也不能再通过 pthread_join 去等待它
    // 这样做的好处：主线程可以专心跑事件循环，不用管这个“Java 逻辑线程”何时退出
    if (pthread_detach(main_thr)) {
        JLI_ReportErrorMessageSys("pthread_detach() failed: %s\n", strerror(errno));
        exit(1);
    }

    // 在主线程中进入 Cocoa 事件循环
    // 真正跑 Java 启动逻辑的是新开的线程（apple_main）
    // ParkEventLoop() 的作用，就是让这个主线程一直跑着不退出
    ParkEventLoop();
}
```
