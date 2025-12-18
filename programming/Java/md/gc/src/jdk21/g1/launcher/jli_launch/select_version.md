# SelectVersion 函数

```cpp
// --- src/java.base/share/native/libjli/java.c --- //

/**
 * 确保运行了合适的 JRE 版本
 * 首先从 JAR 文件中的 MANIFEST.MF 中获取所需的版本信息，
 * 如果 JAR 文件中未提供则从命令行选项中获取
 * 此外，该函数还会解析启动画面(Splash Screen)相关的命令行参数，并通过私有环境变量传递这些值
 *
 * @param argc 命令行参数个数
 * @param argv 命令行参数
 * @param main_class 主类名
 */
static void
SelectVersion(int argc, char **argv, char **main_class) {
    char *arg;
    char *operand;
    int jarflag = 0;
    int headlessflag = 0;
    manifest_info info;
    char *splash_file_name = NULL;
    char *splash_jar_name = NULL;
    char *env_in;
    int res;
    jboolean has_arg;

    // 老版本的 JRE（1.5～1.8），具备某种 "mJRE 能力"
    // 这些老 JRE 可以通过这个环境变量，把启动信息（尤其是主类名）传递给新版本 JRE（1.9+）
    // 新版本启动器这边看到环境变量存在，就直接用这个信息, 不再自己去分析 manifest、mJRE 指令之类的东西
    // 这样，老的 JRE 当成一个 "中介/启动器"，去拉起新版本的 JRE
    if ((env_in = getenv(ENV_ENTRY)) != NULL) {
        if (*env_in != '\0') {
            // main_class 最终指向了环境变量(由ENV_ENTRY宏设置)中指定的主类名
            *main_class = JLI_StringDup(env_in);
        }
        // 老 JRE 已经帮我算好了 main class，那我就相信它，自己不再分析命令行、manifest 等
        return;
    }

    // 处理和 "多 JRE 支持" 有关的选项
    // "多 JRE 支持" 这个功能存在于 JRE 1.5 到 1.8 版本
    // 在 1.9 及之后，这个功能已经取消了
    // 所以一旦匹配到这些老选项，就直接报错，不再继续处理这些选项

    // 跳过第一个参数(通常是程序名，比如 java)
    argc--;
    argv++;
    // 只处理以 - 开头的命令行参数，这种命令行参数称为：选项
    while (argc > 0 && *(arg = *argv) == '-') {
        // 判断当前这个选项是不是会带一个“附加参数”例如：
        // -cp classpath
        // --module-path someDir
        has_arg = IsOptionWithArgument(argc, argv);

        if (JLI_StrCCmp(arg, "-version:") == 0) {
            // 和 "多 JRE 支持" 有关的选项，现在被废弃，遇见了直接报错
            JLI_ReportErrorMessage(SPC_ERROR1);
        } else if (JLI_StrCmp(arg, "-jre-restrict-search") == 0) {
            // 和 "多 JRE 支持" 有关的选项，现在被废弃，遇见了直接报错
            JLI_ReportErrorMessage(SPC_ERROR2);
        } else if (JLI_StrCmp(arg, "-jre-no-restrict-search") == 0) {
            // 和 "多 JRE 支持" 有关的选项，现在被废弃，遇见了直接报错
            JLI_ReportErrorMessage(SPC_ERROR2);
        } else {
            // 处理其他正常的选项

            // 检测当前参数是不是 "-jar"
            if (JLI_StrCmp(arg, "-jar") == 0) {
                // 设置 jarflag = 1 之后 operand 就应该是一个 JAR 文件
                jarflag = 1;
            }
            // 跳过“带参数的选项”的参数值
            // 比如 --module-path someDir 中的 someDir
            if (IsWhiteSpaceOption(arg)) {
                // 跳过当前选项的附加参数
                if (has_arg) {
                    argc--;
                    argv++;
                    arg = *argv;
                }
            }

            if (JLI_StrCmp(arg, "-Djava.awt.headless=true") == 0) {
                // java.awt的无图形界面模式
                headlessflag = 1;
            } else if (JLI_StrCCmp(arg, "-Djava.awt.headless=") == 0) {
                // 只有字符串 "true" 才是真，其他字符串都当作 false
                headlessflag = 0;
            } else if (JLI_StrCCmp(arg, "-splash:") == 0) {
                // 记录启动画面图片的路径
                // 字符串 "-splash:" 的长度是 8
                // 所以 arg + 8 就指向后面的文件名部分，
                // 例如 "-splash:logo.png" 中的 "logo.png"
                splash_file_name = arg + 8;
            }
        }
        argc--;
        argv++;
    }

    // while 处理完所有以 - 开头的参数后，
    // 剩下的第一个非 - 参数就是 operand，用来表示“要运行什么”
    // 1. 如果有 -jar，那就是 JAR 文件名（如 app.jar）
    // 2. 否则通常是主类名（如 com.example.Main），但本函数里只特殊对待 -jar 的情况
    if (argc <= 0) {
        // 可能不存在 operand，比如：
        // 1. java -version
        // 2. java -help
        // 这些不需要类名或 JAR，也是合法的
        operand = NULL;
    } else {
        argc--;
        operand = *argv++;
    }

    // 如果是 -jar 启动，则尝试从该 JAR 文件中读取 MANIFEST.MF
    // 如果从 JAR 文件中读取失败，则报错并退出
    if (jarflag && operand) {
        // 解析 MANIFEST.MF 文件
        if ((res = JLI_ParseManifest(operand, &info)) != 0) {
            // MANIFEST.MF 文件解析失败
            if (res == -1)
                JLI_ReportErrorMessage(JAR_ERROR2, operand);
            else
                JLI_ReportErrorMessage(JAR_ERROR3, operand);
            exit(1);
        }

        // 启动画面优先级：
        // 1. 如果命令行已经通过 -splash:xxx 指定，则 manifest 里的启动画面被忽略。
        // 2. 否则，如果 manifest 里指定了 SplashScreen-Image，且不是 headless 模式，就：
        //    1. 把 splash_file_name 设置为该图片路径
        //    2. 把 splash_jar_name 设置为这个 JAR 的名字（后面写环境变量时要一起传）
        if (!headlessflag && !splash_file_name && info.splashscreen_image_file_name) {
            splash_file_name = info.splashscreen_image_file_name;
            splash_jar_name = operand;
        }
    } else {
        // 如果不是 -jar 或根本没有 operand，则把 info 清空，以防后面误用
        info.manifest_version = NULL;
        info.main_class = NULL;
        info.jre_version = NULL;
        info.jre_restrict_search = 0;
    }

    // 把启动画面信息通过环境变量传出去
    // 构造两个类似 KEY=value 的字符串，然后通过 putenv 写入到当前进程的环境变量
    // 1. 一个是图片路径 SPLASH_FILE_ENV_ENTRY
    // 2. 一个是 JAR 名 SPLASH_JAR_ENV_ENTRY
    // JLI_MemAlloc 分配的内存不会再被释放，因为环境变量需要在整个进程生命周期里有效
    // 这些信息会被后面的 GUI / splashscreen 显示逻辑读取，用来显示启动画面
    if (splash_file_name && !headlessflag) {
        splash_file_entry = JLI_MemAlloc(JLI_StrLen(SPLASH_FILE_ENV_ENTRY "=") + JLI_StrLen(splash_file_name) + 1);
        JLI_StrCpy(splash_file_entry, SPLASH_FILE_ENV_ENTRY "=");
        JLI_StrCat(splash_file_entry, splash_file_name);
        putenv(splash_file_entry);
    }
    if (splash_jar_name && !headlessflag) {
        splash_jar_entry = JLI_MemAlloc(JLI_StrLen(SPLASH_JAR_ENV_ENTRY "=") + JLI_StrLen(splash_jar_name) + 1);
        JLI_StrCpy(splash_jar_entry, SPLASH_JAR_ENV_ENTRY "=");
        JLI_StrCat(splash_jar_entry, splash_jar_name);
        putenv(splash_jar_entry);
    }

    // 如果 manifest 里有 Main-Class 条目，则复制一份保存到 *main_class 中
    if (info.main_class != NULL) {
        *main_class = JLI_StringDup(info.main_class);
    }

    // 如果 manifest 里没有指定 jre_version
    if (info.jre_version == NULL) {
        // 释放内部缓存的 manifest 相关信息
        JLI_FreeManifest();
    }
}
```
