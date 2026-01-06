# 决定用哪个 JVM 类型

```cpp
// --- src/java.base/share/native/libjli/java.c --- //

/**
 * 从命令行参数、环境变量里找出“要用哪种 JVM”（client/server/别名/自定义），
 * 并且把 JVM 相关的参数从 argv 里删掉，最后返回要用的 JVM 类型字符串
 *
 * @param speculative 是否开启试探模式，有问题就返回 "ERROR"，不直接退出程序
 * @return 一个字符串指针，表示最终选中的 JVM 类型，例如 "client"、"server" 或自定义名字
 */
char *
CheckJvmType(int *pargc, char ***argv, jboolean speculative) {
    int i, argi;
    int argc;
    // 新建的参数数组，用来存过滤之后的参数
    char **newArgv;
    // 当前写入 newArgv 的位置索引
    int newArgvIdx = 0;
    int isVMType;
    // 在 knownVMs[] 数组中的索引
    // 表示最终选定要使用 knownVMs[] 中的哪个配置
    // 初始 -1 表示“还没选定配置中的某一条”
    int jvmidx = -1;
    // 初始值来自环境变量 JDK_ALTERNATE_VM，如果设置了，比如 JDK_ALTERNATE_VM=server，优先作为 JVM 类型的候选
    char *jvmtype = getenv("JDK_ALTERNATE_VM");

    argc = *pargc;

    // 复制一份新的 argv
    newArgv = JLI_MemAlloc((argc + 1) * sizeof(char *));

    // argv[0]（程序名）始终保留，放入 newArgv[0]
    newArgv[newArgvIdx++] = (*argv)[0];

    // 遍历命令行参数，识别和剔除 JVM 类型的选项
    for (argi = 1; argi < argc; argi++) {
        char *arg = (*argv)[argi];
        isVMType = 0;

        // 如果 IsJavaArgs 返回 true, 表示当前启动的是 jmap 等 JDK 内置工具
        // 否则表示当前启动的是普通的 java 程序
        if (IsJavaArgs()) {
            if (arg[0] != '-') {
                // 只有以 - 开头的才当作选项
                // 非 - 开头的参数直接拷到 newArgv，不参与 JVM 类型判断
                newArgv[newArgvIdx++] = arg;
                continue;
            }
        } else {
            // 如果 IsWhiteSpaceOption 返回 true, 表示这是某些选项, 形如：-cp 后面还带一个单独参数的情况
            if (IsWhiteSpaceOption(arg)) {
                // 碰到这种，当前选项和后面的一个参数一起拷贝走，不参与 JVM 类型判断
                newArgv[newArgvIdx++] = arg;
                argi++;
                if (argi < argc) {
                    newArgv[newArgvIdx++] = (*argv)[argi];
                }
                continue;
            }
            // 如果参数不是以 - 开头，就认为后面都是应用参数，不再解析 JVM 类型
            if (arg[0] != '-') {
                break;
            }
        }

        // 开始检查 JVM 类型

        // 检查是否是“显式 JVM 类型”参数
        // 在 knownVMs[] 里查这个参数，比如 -client、-server 等，看是不是一个在 jvm.cfg 注册过的名称
        // 若找到了，返回索引 i
        i = KnownVMIndex(arg);
        if (i >= 0) {
            // knownVMs[i].name 的值是类似 "-client" 这样的字符串，
            // 因此 + 1 跳过第一个 -，jvmtype 变成 "client"
            jvmtype = knownVMs[jvmidx = i].name + 1;
            // 表示这个参数是一个 JVM 类型参数，不应该再进 newArgv
            isVMType = 1;
            // 参数个数减一，因为删掉了这个 JVM 类型选项
            *pargc = *pargc - 1;
        }

        // 检查“候选 JVM”参数
        // 支持两种写法：
        // 1. -XXaltjvm=foo
        // 2. -J-XXaltjvm=foo（传给子 JVM 的形式）
        else if (JLI_StrCCmp(arg, "-XXaltjvm=") == 0 || JLI_StrCCmp(arg, "-J-XXaltjvm=") == 0) {
            isVMType = 1;
            // 如果 arg[1] == 'X'，说明是 -XXaltjvm=，此字符串长度是 10，jvmtype 指向 = 后的那一部分，也就是 foo
            // 否则是 -J-XXaltjvm=，前面多了 -J，长度 12，从 12 以后才是 JVM 名
            jvmtype = arg + ((arg[1] == 'X') ? 10 : 12);
            // 表示这个 JVM 名并不是 knownVMs[] 中的某一个配置
            jvmidx = -1;
        }

        // 非 JVM 类型参数
        if (!isVMType) {
            // 如果当前参数既不是 -client/-server 之类，也不是 -XXaltjvm=，就直接保留到 newArgv
            newArgv[newArgvIdx++] = arg;
        }
    }

    // argi < argc 表示参数没遍历完就 break 了
    // 如果中途 break，把后面剩下的参数全部拷贝到 newArgv
    // 确保所有后续参数不丢失
    while (argi < argc) {
        newArgv[newArgvIdx++] = (*argv)[argi];
        argi++;
    }

    // argv 最后要以 \0 结尾
    newArgv[newArgvIdx] = 0;

    // 把处理好的 newArgv 和新长度回写给调用方
    // 此时，所有 JVM 类型相关的参数已经被“吃掉”，不会作为应用参数继续传给 JVM 本身
    *argv = newArgv;
    *pargc = newArgvIdx;

    // 如果没有环境变量，也没有命令行指定 JVM 类型
    // 就使用 knownVMs[0] 作为默认 JVM，比如通常是 "client" 或 "server"。
    if (jvmtype == NULL) {
        // 还是通过 +1 去掉前面的 - 得到真正的类型名
        char *result = knownVMs[0].name + 1;
        JLI_TraceLauncher("Default VM: %s\n", result);
        return result;
    }

    // 不是通过 KnownVMIndex 找到的，而是 JDK_ALTERNATE_VM 或 -XXaltjvm= 指定的
    // 这些“自定义 VM”不会参加 jvm.cfg 里 alias（别名）解析逻辑，直接用用户写的路径/名字
    if (jvmidx < 0)
        return jvmtype;

    // 对通过 jvm.cfg 找到的 JVM 类型进行别名解析
    {
        int loopCount = 0;
        // 如果 knownVMs[jvmidx].flag == VM_ALIASED_TO
        // 表示这个 JVM 不是具体实现，而是别名，需要跟着 alias 跳到另一个条目。
        while (knownVMs[jvmidx].flag == VM_ALIASED_TO) {
            // knownVMs[jvmidx].alias 是它指向的那个 flag（比如 -server）。
            // 用 KnownVMIndex() 找出那个 alias 在 knownVMs[] 中对应的下标 nextIdx。
            int nextIdx = KnownVMIndex(knownVMs[jvmidx].alias);

            // 防止出现循环别名（比如 A 指向 B，B 又指向 A），超过总数认为有环
            // knownVMsCount 是 knownVMs[] 的长度, 在 ReadKnownVMs 函数中设置
            if (loopCount > knownVMsCount) {
                if (!speculative) {
                    JLI_ReportErrorMessage(CFG_ERROR1);
                    exit(1);
                } else {
                    return "ERROR";
                    /* break; */
                }
            }

            // alias 指到了一个不存在的名字
            if (nextIdx < 0) {
                if (!speculative) {
                    JLI_ReportErrorMessage(CFG_ERROR2, knownVMs[jvmidx].alias);
                    exit(1);
                } else {
                    return "ERROR";
                }
            }
            // 一层层解析, 直到 flag 不再是 VM_ALIASED_TO 才停下来
            jvmidx = nextIdx;
            jvmtype = knownVMs[jvmidx].name + 1;
            loopCount++;
        }
    }

    // 根据选定 JVM 类型的 flag 决定最终行为
    switch (knownVMs[jvmidx].flag) {
        case VM_WARN:
            // 打一条警告，告诉你这个 JVM 类型不再推荐或将被淘汰，并提示默认 JVM
            if (!speculative) {
                JLI_ReportErrorMessage(CFG_WARN1, jvmtype, knownVMs[0].name + 1);
            }
        /* fall through */
        case VM_IGNORE:
            // 把 jvmtype 强制改成默认 JVM（knownVMs[0]）
            jvmtype = knownVMs[jvmidx = 0].name + 1;
        /* fall through */
        case VM_KNOWN:
            // 合法的正常 JVM 类型，啥也不做，直接用当前 jvmtype
            break;
        case VM_ERROR:
            // 这个 JVM 类型是“禁止使用”的
            if (!speculative) {
                JLI_ReportErrorMessage(CFG_ERROR3, jvmtype);
                exit(1);
            } else {
                return "ERROR";
            }
    }

    return jvmtype;
}
```
