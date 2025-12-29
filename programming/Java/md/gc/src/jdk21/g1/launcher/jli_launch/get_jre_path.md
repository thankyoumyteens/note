# 找到要使用的 JRE

```cpp
// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

/**
 * 找到 JRE 的路径
 *
 * @param path 一个输出缓冲区，用于存放找到的 JRE 路径
 * @param pathsize path 缓冲区的大小
 * @param speculative 是否是“推测性”查找。如果是 JNI_TRUE，意味着只是尝试一下，找不到也不一定要报错
 */
static jboolean
GetJREPath(char *path, jint pathsize, jboolean speculative)
{
    // 临时缓冲区，用于构建 libjava.dylib 或 jvm.cfg 的路径
    char libjava[MAXPATHLEN];

    // 1. 查找与应用程序同目录的 JRE

    // GetApplicationHome 尝试获取应用程序（比如 java.exe 或 java.so）的安装目录，
    // 并将其存入 path 缓冲区。如果成功，则进入 if
    if (GetApplicationHome(path, pathsize)) {
        /* Is JRE co-located with the application? */
#ifdef STATIC_BUILD
        // 静态构建 (STATIC_BUILD) 的情况
        char jvm_cfg[MAXPATHLEN];
        // 检查 <apphome>/lib/jvm.cfg 是否存在
        JLI_Snprintf(jvm_cfg, sizeof(jvm_cfg), "%s/lib/jvm.cfg", path);
        if (access(jvm_cfg, F_OK) == 0) {
            // 如果 jvm.cfg 存在，说明 JRE 在这里，返回成功
            return JNI_TRUE;
        }
#else
        // 动态构建 (通常情况)
        // JAVA_DLL 在 macOS 平台的取值是 libjava.dylib
        JLI_Snprintf(libjava, sizeof(libjava), "%s/lib/" JAVA_DLL, path);
        // 检查 <apphome>/lib/libjava.dylib 是否存在
        if (access(libjava, F_OK) == 0) {
            // 如果 libjava.dylib 存在，说明 JRE 在这里，返回成功
            return JNI_TRUE;
        }
#endif
        // 检查私有 JRE
        // 检查 path 缓冲区是否足够存储 "path + /jre + \0"
        if ((JLI_StrLen(path) + 4 + 1) > (size_t) pathsize) {
            JLI_TraceLauncher("Insufficient space to store JRE path\n");
            return JNI_FALSE;
        }
        // 检查 <apphome>/jre/lib/libjava.dylib 是否存在
        JLI_Snprintf(libjava, sizeof(libjava), "%s/jre/lib/" JAVA_DLL, path);
        if (access(libjava, F_OK) == 0) {
            // 如果存在，则将 "/jre" 追加到 path 中
            JLI_StrCat(path, "/jre");
            JLI_TraceLauncher("JRE path is %s\n", path);
            return JNI_TRUE;
        }
    }

    // 2. 尝试从自身（启动器）的位置查找 JRE
    // 如果应用程序目录下面没有找到 JRE，那么就从启动器（比如 java 命令本身）的位置来推断 JRE 的位置

    // 用于存储 dladdr 函数返回的信息
    Dl_info selfInfo;
    // dladdr 获取当前函数（GetJREPath）所在的动态库的信息, 写入到 selfInfo 中
    // selfInfo 中的 dli_fname 字段通常包含该动态库的路径
    dladdr(&GetJREPath, &selfInfo);

#ifdef STATIC_BUILD
    // 静态构建 (STATIC_BUILD) 的情况
    char jvm_cfg[MAXPATHLEN];
    char *p = NULL;
    // 复制 dli_fname 到 jvm_cfg
    strncpy(jvm_cfg, selfInfo.dli_fname, MAXPATHLEN);
    // 从路径中移除文件名，得到目录
    // 把最后一个 '/' 替换成 '\0', 相当于移除了它和后面的部分
    p = strrchr(jvm_cfg, '/'); *p = '\0';
    // 再移除上一级目录
    p = strrchr(jvm_cfg, '/'); // 再定位到最后一个 '/'
    // 特殊处理类似 "/bin/." 的情况
    if (strcmp(p, "/.") == 0) {
        *p = '\0'; // 移除 "/."
        p = strrchr(jvm_cfg, '/'); *p = '\0'; // 再移除最后一个 '/' 和后面的部分
    }
    else {
        // 直接移除最后一个 '/' 和后面的部分
        *p = '\0';
    }
    // 将处理后的路径（推测是 JRE 的根目录）复制到 path
    strncpy(path, jvm_cfg, pathsize);
    // 拼接 jvm.cfg 的路径
    strncat(jvm_cfg, "/lib/jvm.cfg", MAXPATHLEN);
    // 检查 jvm.cfg 是否存在
    if (access(jvm_cfg, F_OK) == 0) {
        // 如果 jvm.cfg 存在，说明 JRE 在这里，返回成功
        return JNI_TRUE;
    }
#endif
    // 处理动态构建的情况

    // 使用 realpath 获取当前加载的库 (libjli.dylib) 的绝对路径
    // realpath 函数正常执行后, 返回值 realPathToSelf 和第二个参数 path 是同一个指针
    char *realPathToSelf = realpath(selfInfo.dli_fname, path);
    // 检查 realpath 函数是否成功(realpath 是否和 path 指向同一个地方)
    if (realPathToSelf != path) {
        return JNI_FALSE;
    }

    // 获取库的绝对路径长度
    size_t pathLen = strlen(realPathToSelf);
    if (pathLen == 0) {
        return JNI_FALSE;
    }

    // 定义 JRE lib 目录的常见路径模式 (macOS 的 JRE 结构)
    const char lastPathComponent[] = "/lib/libjli.dylib";
    size_t sizeOfLastPathComponent = sizeof(lastPathComponent) - 1;
    // 检查当前路径是否足够长以包含这个模式
    if (pathLen < sizeOfLastPathComponent) {
        return JNI_FALSE;
    }

    // 计算模式开始的位置
    size_t indexOfLastPathComponent = pathLen - sizeOfLastPathComponent;
    // 检查 realPathToSelf 的末尾是不是 "/lib/libjli.dylib"
    if (0 == strncmp(realPathToSelf + indexOfLastPathComponent, lastPathComponent, sizeOfLastPathComponent)) {
        // 如果匹配，说明 libjli.dylib 在 JRE 的 lib 目录下
        // 将路径截断到 JRE 的根目录 (移除 "/lib/libjli.dylib")
        realPathToSelf[indexOfLastPathComponent + 1] = '\0';
        return JNI_TRUE;
    }

    // 特殊处理 macOS bundle 结构(jre 被打包成 macOS 的 APP 了)
    // JRE 可能位于 <app_bundle>.app/Contents/MacOS/libjli.dylib，或者 <app_bundle>.app/Contents/Home/lib/libjli.dylib
    // 这里的逻辑是检查是否以 "/MacOS/libjli.dylib" 结尾
    const char altLastPathComponent[] = "/MacOS/libjli.dylib";
    size_t sizeOfAltLastPathComponent = sizeof(altLastPathComponent) - 1;
    if (pathLen < sizeOfLastPathComponent) {
        return JNI_FALSE;
    }

    // 检查路径末尾是否匹配 "/MacOS/libjli.dylib"
    size_t indexOfAltLastPathComponent = pathLen - sizeOfAltLastPathComponent;
    if (0 == strncmp(realPathToSelf + indexOfAltLastPathComponent, altLastPathComponent, sizeOfAltLastPathComponent)) {
        // 如果匹配，尝试将路径修改为指向 "/Home" 目录: <app_bundle>.app/Contents/Home
        JLI_Snprintf(realPathToSelf + indexOfAltLastPathComponent, sizeOfAltLastPathComponent, "%s", "/Home");
        // 检查这个 "/Home" 目录是否存在
        if (access(realPathToSelf, F_OK) == 0) {
            return JNI_TRUE;
        }
    }

    // 如果没启用推测性查找，报错: JRE 没找到
    if (!speculative) {
        JLI_ReportErrorMessage(JRE_ERROR8 JAVA_DLL);
    }
    return JNI_FALSE;
}
```

## GetApplicationHome

```cpp
// --- src/java.base/unix/native/libjli/java_md_common.c --- //

jboolean
GetApplicationHome(char *buf, jint bufsize) {
    const char *execname = GetExecName();
    if (execname != NULL) {
        JLI_Snprintf(buf, bufsize, "%s", execname);
        buf[bufsize - 1] = '\0';
    } else {
        return JNI_FALSE;
    }
    // 截取到应用程序的家目录
    return TruncatePath(buf, JNI_FALSE);
}

// --- src/java.base/macosx/native/libjli/java_md_macosx.m --- //

const char *
GetExecName() {
    // 返回在 SetExecname 函数中设置的可执行程序名
    return execname;
}
```
