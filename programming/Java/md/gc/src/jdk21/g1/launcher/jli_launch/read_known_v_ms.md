# 解析 jvm.cfg

```cpp
// --- src/java.base/share/native/libjli/java.c --- //

/**
 * 读取 jvm.cfg 文件，把里边配置的各种 JVM“名字/别名/行为”解析出来，填进一个全局数组 knownVMs[] 里。
 * 后面当用户用 -server、-client 等参数启动时，就根据这里的配置选择具体的 JVM 实现目录、是否报警、是否报错等
 *
 * jvm.cfg 文件的每行格式大致是:
 * -flag   KNOWN
 * -flag   WARN
 * -flag   IGNORE
 * -flag   ERROR
 * -flag   ALIASED_TO     -otherFlag
 * -flag   IF_SERVER_CLASS -server
 *
 * KNOWN：这是一个“已知的 JVM 名字”，其目录名就是这个 flag 去掉 - 后的标识符。
 * ALIASED_TO：flag1 ALIASED_TO flag2，表示 flag1 是 flag2 的别名。
 * WARN：当用户用这个 flag 选 JVM 时，可以用，但要打印警告。
 * IGNORE：认得这个 flag，但忽略它，转而用默认 JVM。
 * ERROR：如果用户用了这个 flag，要报错。
 * IF_SERVER_CLASS：根据是否为“server class machine”（大内存服务器之类）来选择一个 JVM 名；
 *                  在这段代码里标注为 “ignored”，意味着这里并不实现这个逻辑，或只在特殊位置才会用。
 *
 * @param jvmCfgName jvm.cfg 文件路径
 * @param speculative 是否是“推测性”查找。如果是 JNI_TRUE，意味着只是尝试一下，找不到也不一定要退出程序
 * @return
 */
jint
ReadKnownVMs(const char *jvmCfgName, jboolean speculative) {
    FILE *jvmCfg;
    char line[MAXPATHLEN + 20];
    // 当前解析到的 VM 数目
    int cnt = 0;
    // 行号
    int lineno = 0;
    jlong start = 0, end = 0;
    // 当前行解析出的 VM 类型（KNOWN / WARN / IGNORE / ...）
    int vmType;
    char *tmpPtr;
    // 如果是 ALIASED_TO，记录别名目标的 VM 名
    char *altVMName = NULL;
    // 空格和制表符
    static char *whiteSpace = " \t";

    // 如果打开了 trace（调试）模式，就记一下开始时间，用于统计解析耗时
    if (JLI_IsTraceLauncher()) {
        start = CurrentTimeMicros();
    }

    // 打开 jvm.cfg 文件
    jvmCfg = fopen(jvmCfgName, "r");
    if (jvmCfg == NULL) {
        if (!speculative) {
            JLI_ReportErrorMessage(CFG_ERROR6, jvmCfgName);
            exit(1);
        } else {
            // 如果开启了“推测性”查找
            // 返回 -1，交给上层决定后续逻辑
            return -1;
        }
    }
    // 逐行读取并解析
    while (fgets(line, sizeof(line), jvmCfg) != NULL) {
        vmType = VM_UNKNOWN;
        lineno++;
        // 以 # 开头的是注释，直接跳过
        if (line[0] == '#') {
            continue;
        }
        // flag 在语法上必须是 -xxx 形式
        if (line[0] != '-') {
            // 不以 - 开头则发出警告（但仍继续往下试图解析这一行）
            JLI_ReportErrorMessage(CFG_WARN2, lineno, jvmCfgName);
        }
        // 如果已用满当前 knownVMs 容量，就扩容
        if (cnt >= knownVMsLimit) {
            GrowKnownVMs(cnt);
        }
        // 去掉结尾的换行符
        // fgets 会保留 \n，这里直接把最后一个字符改成 \0
        line[JLI_StrLen(line) - 1] = '\0';
        // 找到 flag 后面的第一个空白
        // JLI_StrCSpn: 找到第一个属于 " " 或 "\t" 字符位置
        // line 只想这一行的起始位置
        // 于是 tmpPtr 指向 flag 后面的第一个空格或制表符
        tmpPtr = line + JLI_StrCSpn(line, whiteSpace);
        if (*tmpPtr == 0) {
            // 情况1: 没有找到空白（比如只有 -client）
            // 发出警告
            JLI_ReportErrorMessage(CFG_WARN3, lineno, jvmCfgName);
        } else {
            // 把空白变成 '\0'，把 flag 单独变成一个 C 字符串
            *tmpPtr++ = 0;
            // 跳过后面的连续空白
            tmpPtr += JLI_StrSpn(tmpPtr, whiteSpace);
            if (*tmpPtr == 0) {
                // 情况2: 找到空白，但后面只有空白（没有类型单词 KNOWN 等）
                // 也警告
                JLI_ReportErrorMessage(CFG_WARN3, lineno, jvmCfgName);
            } else {
                // 情况3: 正确的语法
                // 把类型设置到 vmType
                if (!JLI_StrCCmp(tmpPtr, "KNOWN")) {
                    vmType = VM_KNOWN;
                } else if (!JLI_StrCCmp(tmpPtr, "ALIASED_TO")) {
                    // ALIASED_TO 后面必须还要有一个 flag(别名)
                    // 先跳到 "ALIASED_TO" 后面的空白字符
                    tmpPtr += JLI_StrCSpn(tmpPtr, whiteSpace);
                    // 跳过空白，到达第三个 token
                    if (*tmpPtr != 0) {
                        tmpPtr += JLI_StrSpn(tmpPtr, whiteSpace);
                    }
                    if (*tmpPtr == 0) {
                        // 如果没第三个 token, 警告
                        JLI_ReportErrorMessage(CFG_WARN3, lineno, jvmCfgName);
                    } else {
                        // 把这个第三个 token 作为别名(altVMName)，并在它后面的空白处放 \0，变成独立字符串
                        altVMName = tmpPtr;
                        tmpPtr += JLI_StrCSpn(tmpPtr, whiteSpace);
                        *tmpPtr = 0;
                        vmType = VM_ALIASED_TO;
                    }
                } else if (!JLI_StrCCmp(tmpPtr, "WARN")) {
                    vmType = VM_WARN;
                } else if (!JLI_StrCCmp(tmpPtr, "IGNORE")) {
                    vmType = VM_IGNORE;
                } else if (!JLI_StrCCmp(tmpPtr, "ERROR")) {
                    vmType = VM_ERROR;
                } else if (!JLI_StrCCmp(tmpPtr, "IF_SERVER_CLASS")) {
                    /* ignored */
                } else {
                    // 警告
                    JLI_ReportErrorMessage(CFG_WARN5, lineno, &jvmCfgName[0]);
                    // 仍然把这一行当作 VM_KNOWN 处理（一个兜底行为）
                    vmType = VM_KNOWN;
                }
            }
        }

        // 打印调试日志
        JLI_TraceLauncher("jvm.cfg[%d] = ->%s<-\n", cnt, line);
        // 把解析结果存入 knownVMs[]
        if (vmType != VM_UNKNOWN) {
            // 这里的 line 现在只包含第一个 token，即 flag 名（如 "-client"）
            knownVMs[cnt].name = JLI_StringDup(line);
            knownVMs[cnt].flag = vmType;
            switch (vmType) {
                default:
                    break;
                case VM_ALIASED_TO:
                    // 如果是别名行，还会设置 knownVMs[cnt].alias 为被指向的 VM 名字，比如 "-server"
                    knownVMs[cnt].alias = JLI_StringDup(altVMName);
                    JLI_TraceLauncher("    name: %s  vmType: %s  alias: %s\n",
                                      knownVMs[cnt].name, "VM_ALIASED_TO", knownVMs[cnt].alias);
                    break;
            }
            cnt++;
        }
    }
    fclose(jvmCfg);
    // 记录总共多少个条目
    knownVMsCount = cnt;

    // 如果开启了 trace，打印解析耗时
    if (JLI_IsTraceLauncher()) {
        end = CurrentTimeMicros();
        printf("%ld micro seconds to parse jvm.cfg\n", (long) (end - start));
    }

    // 返回一共解析到多少个已知 VM 条目
    return cnt;
}
```
