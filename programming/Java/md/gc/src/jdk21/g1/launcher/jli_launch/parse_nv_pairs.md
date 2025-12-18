# 解析出键值对

```cpp
// --- src/java.base/share/native/libjli/parse_manifest.c --- //

/**
 * 从 Manifest 的内容中解析出一对 name/value
 * MANIFEST.MF 的组成：
 * - 若干段（section）
 * - 每个 section 包含多行 Name: Value 形式的属性
 * 核心规则：
 * 1. 每一行是：属性名: 空格 + 属性值
 * 2. 行最大长度：不得超过 72 字符，超过会自动被换行。续行以一个空格开头，表示是上一行的延续
 * 3. 每个 section（段）之间用一个空行分隔
 * 4. 文件最后必须以换行结束
 *
 * @param lp 当前指向 Manifest 中某个位置，从这里开始尝试解析一条 name: value 形式的键值对
 * @param name 指向解析出的名字（以 '\0' 结尾）
 * @param value 指向解析出的值（同样 '\0' 结尾）
 * @return 1：成功解析到一对 name/value
 *         0：遇到一个“空行”或字符串结束，表示当前 section 结束（不是错误）
 *        -1：格式非法或出错
 */
static int
parse_nv_pair(char **lp, char **name, char **value) {
    char *nl;
    char *cp;

    // 检查是否到达 section 末尾
    // *lp 是当前解析的位置, **lp 就是当前位置那个字符
    // 如果是：
    // 1. '\0'：字符串结束（Manifest “串”结束）
    // 2. '\n' 或 '\r'：空行（只包含换行符）
    // 这些情况都表示：当前 section 结束了，返回 0，上层代码看到返回 0 就知道：“本 section 读完了”
    if (**lp == '\0' || **lp == '\n' || **lp == '\r') {
        return (0);
    }

    // 到这里说明这行不是空行，开始解析 name/value

    // 找到当前行的“行尾”：\n 或 \r
    // strpbrk()的参数
    // 1. 要被检索的 C 字符串。
    // 2. 该字符串包含了要在参数 1 中进行匹配的字符列表
    nl = JLI_StrPBrk(*lp, "\n\r");
    if (nl == NULL) {
        // 如果没找到任何换行符（nl == NULL），
        // 那就找到字符串末尾 '\0' 作为行尾（不太正常，但做个容错）
        nl = JLI_StrChr(*lp, (int) '\0');
    } else {
        // 找到了换行符
        // 把 cp 设成当前行尾的位置，后面会用它来“合并续行”
        cp = nl; /* For merging continuation lines */
        // 如果是 \r\n 这种 Windows 风格换行
        if (*nl == '\r' && *(nl + 1) == '\n') {
            // 把 '\r' 先改成 '\0'，然后 nl++ 跳到 '\n'
            *nl++ = '\0';
        }
        // 然后对这个行尾再做一次 *nl++ = '\0'
        // 相当于：给当前这一行加上字符串结束符 '\0'，并且让 nl 指向下一行的开头
        *nl++ = '\0';
        // 此时:
        // - *lp 到 cp 之间，是这一行的内容，已经是一个 C 字符串
        // - nl 指向下一行的开头（可能是续行，也可能是下一个新行或空行）

        // 处理续行（continuation lines）
        // while (*nl == ' ')：只要下一行的第一个字符是空格，就处理一整行续行
        while (*nl == ' ') {
            // 跳过这一行的第一个空格
            nl++; /* First character to be moved */
            // 从当前 nl 开始，一直复制字符到 cp（上一次行尾的位置），直到遇到换行或字符串结束。
            // 这一步完成后，续行的文本就被追加到原来的行后面了
            while (*nl != '\n' && *nl != '\r' && *nl != '\0') {
                *cp++ = *nl++; /* Shift string */
            }
            // 如果直接遇到 '\0'，说明缺少换行，格式错误
            if (*nl == '\0') {
                return (-1); /* Error: newline required */
            }
            // 把现在的“合并后整行”变成一个 C 字符串结尾
            *cp = '\0';
            // 处理Windows 的 CRLF 的情况，把 \r 变成 '\0'，再 nl++ 跳过 \n，最后再 *nl++ = '\0'
            if (*nl == '\r' && *(nl + 1) == '\n') {
                *nl++ = '\0';
            }
            // 使这行结束并把 nl 移到下一行开头
            *nl++ = '\0';
        }
    }

    // 分离 name 和 value

    // 找到 : 的位置，这是 name 与 value 的分隔符
    cp = JLI_StrChr(*lp, (int) ':');
    // 找不到则表示格式不合法
    if (cp == NULL) {
        return (-1);
    }
    // 把这个 ':' 改成 '\0'
    // *lp 到这个位置就形成了 name 的内容
    *cp++ = '\0';
    // 按规范，: 后面必须紧接一个空格。如果不是空格，格式错误
    if (*cp != ' ') {
        return (-1);
    }
    // 把这个空格也变成 '\0' 相当于“吃掉”这个空格
    // 现在 cp 指向 value 内容的第一个字符
    *cp++ = '\0';
    // 把结果输出给调用者
    *name = *lp;
    *value = cp;
    *lp = nl;
    return (1);
}
```
