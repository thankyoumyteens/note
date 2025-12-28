# 记录当前可执行文件的名字

```cpp
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

/**
 * 找到当前 Java 启动器（java 命令本身）可执行文件的绝对路径
 *
 * @param argv main 函数传进来的 argv，里面第一个元素 argv[0] 通常就是启动命令的名字
 * @return 可执行文件的绝对路径
 */
const char*
SetExecname(char **argv)
{
    char* exec_path = NULL;
    // 尝试用 dladdr 获取可执行文件信息
    {
        Dl_info dlinfo; // 用于接收 dladdr 返回的信息

        // 获取一个“锚点”地址: fptr
#ifdef STATIC_BUILD
        // 如果是静态编译，直接用 SetExecname 函数自身的地址
        void *fptr;
        fptr = (void *)&SetExecname;
#else
        // 动态库情况：找到 main 函数的地址
        // RTLD_DEFAULT 会在所有加载的动态库里搜索 "main" 符号
        int (*fptr)();
        fptr = (int (*)())dlsym(RTLD_DEFAULT, "main");
#endif
        // 检查 dlsym 是否成功
        if (fptr == NULL) {
            JLI_ReportErrorMessage(DLL_ERROR3, dlerror()); // 报告错误，dlerror() 获取具体错误信息
            return JNI_FALSE; // 返回错误指示 (这里返回 JNI_FALSE 感觉不太对，应该返回 NULL 或者错误码)
        }

        // dladdr(地址, &dlinfo)
        // 作用：根据一个函数地址 (fptr)，获取包含这个函数的动态库 (dlinfo.dli_fname) 的名字
        // 以及该函数在库里的偏移量等信息。
        if (dladdr((void*)fptr, &dlinfo)) {
            // 如果 dladdr 成功，dlinfo.dli_fname 就包含了可执行文件或动态库的名字
            // 注意：在 Solaris 9+ 和 Linux 上，dlinfo.dli_fname 通常已经是绝对路径了。
            // 但为了兼容老系统或不确定性，下面的 realpath 会尝试将其解析为绝对路径。

            char *resolved = (char*)JLI_MemAlloc(PATH_MAX+1); // 分配内存，PATH_MAX 是一个系统定义的路径最大长度
            if (resolved != NULL) {
                // realpath(输入路径, 输出缓冲区)
                // 作用：将一个可能包含相对路径、符号链接的路径，转换为一个绝对路径
                exec_path = realpath(dlinfo.dli_fname, resolved);
                if (exec_path == NULL) {
                    // 如果 realpath 失败（比如 dlinfo.dli_fname 本身就是个坏路径），则释放内存
                    JLI_MemFree(resolved);
                }
            }
        }
    }
    // 这是后备方案。如果 dladdr 加上 realpath 找不到，就用 FindExecName 这个辅助函数寻找
    if (exec_path == NULL) {
        exec_path = FindExecName(argv[0]);
    }
    // 把找到的绝对路径存到全局静态变量 execname 里
    // 方便其他函数随时取用
    execname = exec_path;
    return exec_path;
}
```

## FindExecName

```cpp
// --- src/java.base/unix/native/libjli/java_md_common.c --- //

/**
 * 根据传入的程序名（program），在各种可能的路径下去查找它的绝对路径
 * 它会尝试几种情况：
 * 1. 绝对路径：如果 program 本身就是绝对路径（比如 /usr/bin/java 或 C:\Program Files\Java\bin\java.exe），直接解析返回
 * 2. 相对路径：如果 program 是相对路径（比如 java 或 bin/java），它会先获取当前工作目录 (getcwd)，然后拼接起来再解析
 * 3. 环境变量 PATH：如果 program 看起来不像路径（比如直接就是 java），它就会去 PATH 环境变量里定义的每个目录里去查找
 */
char *
FindExecName(char *program) {
    // 缓冲区，用于存储当前工作目录
    char cwdbuf[PATH_MAX + 2];
    // 指向 PATH 环境变量的字符串
    char *path;
    // PATH 环境变量的临时副本，因为要分割它
    char *tmp_path;
    // 用于在 PATH 字符串中遍历
    char *f;
    // 存储最终找到的绝对路径，初始为 NULL
    char *result = NULL;

    // 检查是否是绝对路径
    // FILE_SEPARATOR 通常是 '/' (Unix) 或 '\' (Windows)
    // JLI_StrRChr(program, ':') 用于检查 Windows 上的盘符，如 "C:"
    if (*program == FILE_SEPARATOR || (FILE_SEPARATOR == '\\' && JLI_StrRChr(program, ':'))) {
        // 如果是绝对路径，则调用 Resolve 解析。
        // Resolve 会处理掉 "." 和 ".." 等，返回规范化的绝对路径。
        // program + 1 是为了跳过第一个字符，比如 '/' 或 'C'，因为 Resolve 会自己加上。
        return Resolve("", program + 1);
    }

    // 检查是否是相对路径
    // JLI_StrRChr(program, FILE_SEPARATOR) 查找最后一个路径分隔符
    if (JLI_StrRChr(program, FILE_SEPARATOR) != NULL) {
        // 如果找到了路径分隔符，说明它是一个相对路径 (e.g., "bin/java")
        // getcwd 获取当前工作目录，然后 Resolve 组合成绝对路径
        return Resolve(getcwd(cwdbuf, sizeof(cwdbuf)), program);
    }

    // 如果前面都不是，就认为它在 PATH 环境变量里查找
    path = getenv("PATH"); // 获取 PATH 环境变量
    if (!path || !*path) {
        // 如果 PATH 为空或不存在
        path = "."; // 默认在当前目录查找
    }

    // 复制 PATH 环境变量，因为我们要分割它，不能直接修改原始环境变量
    // +2 是为了 FILE_SEPARATOR 和 '\0'
    tmp_path = JLI_MemAlloc(JLI_StrLen(path) + 2);
    JLI_StrCpy(tmp_path, path);

    // 遍历 PATH 中的每个目录
    for (f = tmp_path; *f && result == NULL;) {
        // 只要还没找到结果，就继续循环
        char *s = f; // s 指向当前 PATH 目录的开始

        // 找到下一个环境变量的分隔符 PATH_SEPARATOR (Unix 是 ':'，Windows 是 ';')
        // 或者到字符串末尾
        while (*f && (*f != PATH_SEPARATOR)) ++f;

        // 如果找到了 PATH_SEPARATOR，将其替换为 '\0'，实现字符串分割
        // f++ 指向下一个目录的开始
        if (*f) *f++ = '\0';

        // 检查找到的目录 s
        if (*s == FILE_SEPARATOR) {
            // 如果 PATH 中的目录本身就是绝对路径 (e.g., /usr/bin)
            // 直接用 Resolve 拼接上 program
            result = Resolve(s, program);
        } else {
            // 如果 PATH 中的目录是相对路径 (e.g., "bin" 在 PATH 中)
            // 需要先获取当前工作目录，然后拼接
            char dir[2 * PATH_MAX]; // 足够大的缓冲区来存储 "cwd/s"
            // JLI_Snprintf 格式化成 "当前工作目录/PATH中的目录"
            JLI_Snprintf(dir, sizeof(dir), "%s%c%s",
                         getcwd(cwdbuf, sizeof(cwdbuf)), // 获取当前工作目录
                         FILE_SEPARATOR, s); // 加上分隔符和 PATH 中的目录名
            // 然后用 Resolve 拼接上 program
            result = Resolve(dir, program);
        }

        // 如果 Resolve 找到了，就跳出循环
        if (result != NULL) break;
    }

    JLI_MemFree(tmp_path); // 释放 PATH 副本的内存
    return result; // 返回找到的绝对路径，如果没找到就是 NULL
}
```

## Resolve

```cpp
// --- src/java.base/unix/native/libjli/java_md_common.c --- //

/**
 * 将一个目录 (indir) 和一个命令名 (cmd) 拼接起来，形成一个完整的路径，
 * 然后检查这个路径是不是一个可执行的程序（ProgramExists），
 * 最后用 realpath 获取该命令的绝对路径
 */
static char *
Resolve(char *indir, char *cmd) {
    // 缓冲区，用于存储拼接后的路径 (目录 + 分隔符 + 命令名)
    char name[PATH_MAX + 1];
    // 指向最终要返回的绝对路径的指针
    char *real;
    // JLI_Snprintf 的返回值，用于检查是否溢出
    int snprintf_result;

    // 将 indir、文件分隔符 (FILE_SEPARATOR，如 '/' 或 '\') 和 cmd 拼接成一个完整的路径，存入 name 缓冲区。
    snprintf_result = JLI_Snprintf(name, sizeof(name), "%s%c%s", indir, FILE_SEPARATOR, cmd);

    // 检查拼接结果是否有效
    // snprintf_result < 0 表示格式化出错
    // snprintf_result >= sizeof(name) 表示缓冲区溢出（虽然 name 已经加了 1，但这里还是保险起见）
    if ((snprintf_result < 0) || (snprintf_result >= (int) sizeof(name))) {
        return NULL;
    }

    // 检查文件是否存在
    // ProgramExists(name) 会检查 name 指向的文件路径是否存在
    // 并检查它是不是一个可执行文件
    if (!ProgramExists(name)) return NULL;

    // 将 name（可能是相对路径）转换成一个绝对路径，并存入 real 缓冲区。
    // real 需要足够大来存放绝对路径。这里分配了 PATH_MAX + 2 的空间。
    real = JLI_MemAlloc(PATH_MAX + 2);
    if (!realpath(name, real)) {
        // realpath 可能会失败（比如权限问题），如果失败了
        // 就直接复制原始路径（不保证是绝对路径，但至少有个值）
        JLI_StrCpy(real, name);
    }
    // 无论 realpath 是否成功，都返回 real 指针
    return real;
}
```
