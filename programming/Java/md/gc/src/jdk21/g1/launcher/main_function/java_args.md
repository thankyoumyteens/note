# JAVA_ARGS 宏

```cpp
// --- src/java.base/share/native/launcher/defines.h --- //

#ifdef JAVA_ARGS
    // 如果定义了 JAVA_ARGS，表示这是一个JDK内置工具的启动器（如 jdb、javac、jinfo 等）
    #ifdef PROGNAME
        // 程序名称常量
        static const char* const_progname = PROGNAME;
    #else
        // 如果没有定义 PROGNAME，设为 NULL
        static char* const_progname = NULL;
    #endif
    // 主要 Java 参数数组
    static const char* const_jargs[] = JAVA_ARGS;
    #ifdef EXTRA_JAVA_ARGS
        // 额外 Java 参数数组
        static const char* const_extra_jargs[] = EXTRA_JAVA_ARGS;
    #else
        // 如果没有额外参数，设为 NULL
        static const char** const_extra_jargs = NULL;
    #endif
#else
    // 如果没有定义 JAVA_ARGS，表示这是普通的 java 程序的启动器(java)
    #ifdef EXTRA_JAVA_ARGS
        // 错误：EXTRA_JAVA_ARGS 必须和 JAVA_ARGS 一起定义, 不能单独定义
        #error "EXTRA_JAVA_ARGS defined without JAVA_ARGS"
    #endif
    // 默认程序名称为 "java"
    static const char *const_progname = "java";
    // 主要 Java 参数设为 NULL
    static const char **const_jargs = NULL;
    // 额外 Java 参数设为 NULL
    static const char **const_extra_jargs = NULL;
#endif
```

JAVA_ARGS 宏是通过编译器的命令行参数直接定义的，无需在代码文件中显式声明。

例如：

```sh
# 示例, 实际不会用这种方式使用
g++ -DJAVA_ARGS=1 ...
```

## 生成 java 命令(不定义 JAVA_ARGS)

下面的命令会编译出 java 命令的目标文件:

```sh
/usr/bin/clang \
    ...\
    -std=c11 \
    -arch arm64 \
    -D_LITTLE_ENDIAN \
    -DARCH='"aarch64"' \
    -Daarch64 \
    -D_LP64=1 \
    ... \
    -DVERSION_FEATURE=21 \
    -DVERSION_INTERIM=0 \
    -DVERSION_UPDATE=0 \
    -DVERSION_PATCH=0 \
    -DVERSION_EXTRA1=0 \
    -DVERSION_EXTRA2=0 \
    -DVERSION_EXTRA3=0 \
    -DVERSION_PRE='"internal"' \
    -DVERSION_BUILD= \
    -DVERSION_OPT='"adhoc.walter.openjdk"' \
    -DVERSION_NUMBER='"21"' \
    -DVERSION_STRING='"21-internal-adhoc.walter.openjdk"' \
    -DVERSION_SHORT='"21-internal"' \
    -DVERSION_SPECIFICATION='"21"' \
    -DVERSION_DATE='"2023-09-19"' \
    -DVENDOR_VERSION_STRING='""' \
    -DVERSION_CLASSFILE_MAJOR=65 \
    -DVERSION_CLASSFILE_MINOR=0 \
    -DVENDOR_URL='"https://openjdk.org/"' \
    -DVENDOR_URL_BUG='"https://bugreport.java.com/bugreport/"' \
    -DVENDOR_URL_VM_BUG='"https://bugreport.java.com/bugreport/crash.jsp"' \
    -DLAUNCHER_NAME='"openjdk"' \
    # 指定程序名
    -DPROGNAME='"java"' \
    -DEXPAND_CLASSPATH_WILDCARDS \
    -DENABLE_ARG_FILES \
    ...\
    -O0 \
    -c \
    -o /mysrc/openjdk/build/macosx-aarch64-server-slowdebug/support/native/java.base/java/main.o \
    /mysrc/openjdk/src/java.base/share/native/launcher/main.c \
    -frandom-seed="main.c"
```

大量 `-D<NAME>=<VALUE>` 宏：定义 OpenJDK 的版本、特性和路径信息，例如：

- `VERSION_STRING='"21-internal-adhoc.walter.openjdk"'`：JDK 版本字符串（此处为本地编译的内部版本）
- `LAUNCHER_NAME='"openjdk"'`、`PROGNAME='"java"'`：启动器名称（如 java 命令）
- `EXPAND_CLASSPATH_WILDCARDS`：启用类路径通配符扩展（支持 \*.jar 语法）

## 生成 jinfo 命令(定义 JAVA_ARGS)

下面的命令会编译出 jinfo 命令的目标文件:

```sh
/usr/bin/clang \
    ...\
    -std=c11 \
    -arch arm64 \
    -D_LITTLE_ENDIAN \
    -DARCH='"aarch64"' \
    -Daarch64 \
    -D_LP64=1 \
    ... \
    -DVERSION_FEATURE=21 \
    -DVERSION_INTERIM=0 \
    -DVERSION_UPDATE=0 \
    -DVERSION_PATCH=0 \
    -DVERSION_EXTRA1=0 \
    -DVERSION_EXTRA2=0 \
    -DVERSION_EXTRA3=0 \
    -DVERSION_PRE='"internal"' \
    -DVERSION_BUILD= \
    -DVERSION_OPT='"adhoc.walter.openjdk"' \
    -DVERSION_NUMBER='"21"' \
    -DVERSION_STRING='"21-internal-adhoc.walter.openjdk"' \
    -DVERSION_SHORT='"21-internal"' \
    -DVERSION_SPECIFICATION='"21"' \
    -DVERSION_DATE='"2023-09-19"' \
    -DVENDOR_VERSION_STRING='""' \
    -DVERSION_CLASSFILE_MAJOR=65 \
    -DVERSION_CLASSFILE_MINOR=0 \
    -DVENDOR_URL='"https://openjdk.org/"' \
    -DVENDOR_URL_BUG='"https://bugreport.java.com/bugreport/"' \
    -DVENDOR_URL_VM_BUG='"https://bugreport.java.com/bugreport/crash.jsp"' \
    -DLAUNCHER_NAME='"openjdk"' \
    -DPROGNAME='"jinfo"' \
    # 设置JAVA_ARGS宏
    -DJAVA_ARGS='{ "-J-Dsun.jvm.hotspot.debugger.useProcDebugger", "-J-Dsun.jvm.hotspot.debugger.useWindbgDebugger", "-J-ms8m", "-m", "jdk.jcmd/sun.tools.jinfo.JInfo", }' \
    ... \
    -c \
    -o /mysrc/openjdk/build/macosx-aarch64-server-slowdebug/support/native/jdk.jcmd/jinfo/main.o \
    /mysrc/openjdk/src/java.base/share/native/launcher/main.c \
    -frandom-seed="main.c"
```

jinfo 工具专属核心配置:

- `-DPROGNAME='"jinfo"'`：指定启动器名称为 jinfo，即最终生成的可执行命令名。
- `-DJAVA_ARGS='{ ... }'`：这是 jinfo 工具的核心启动参数，本质是给底层 JVM 传递的参数数组，含义如下：
  - `-J-Dsun.jvm.hotspot.debugger.useProcDebugger`：类 Unix 系统（如 Linux/macOS）中使用 proc 调试接口，获取目标 Java 进程的底层信息
  - `-J-Dsun.jvm.hotspot.debugger.useWindbgDebugger`：Windows 系统中使用 Windbg 调试接口（跨平台兼容配置）
  - `-J-ms8m`：设置 JVM 初始堆大小为 8MB（-J 表示给 JVM 传递参数）
  - `-m jdk.jcmd/sun.tools.jinfo.JInfo`：指定模块化应用的主类，即 jinfo 工具的 Java 入口类（属于 jdk.jcmd 模块）
