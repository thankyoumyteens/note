# 在 jar 包中定位到 MANIFEST.MF 文件

```cpp
// --- src/java.base/share/native/libjli/parse_manifest.c --- //

// 读取中央目录时使用的缓冲区大小
// 因为一个中央目录条目中有 3 个可变长字段:
// 1. 文件名（name）
// 2. 额外字段（extra）
// 3. 备注（comment）
// 每个最大可到 64K (2^16=65536)
// CENHDR 表示其余定长字段的总大小 46 字节
// 所以最坏情况下，一个记录长度 ≈ CENHDR + 3 * 64K
// 再加上下一个记录的签名字段 SIGSIZ(4 字节)
// 注意: 现实中通常只用到很小一部分缓冲区，
// 比如只需要读取前两个 Entry（常见为 JAR 的 META-INF/ 和 META-INF/MANIFEST.MF），
// 所以这个缓冲区虽然分配得很大，但大多时候不会真正“触发”所有页面读入内存
#define BUFSIZE (3 * 65536 + CENHDR + SIGSIZ)
#define MINREAD 1024

/**
 * 在 jar(或zip) 文件中寻找 MANIFEST.MF 文件
 *
 * @param fd JAR 文件的文件描述符
 * @param entry 输出参数: MANIFEST.MF 文件的 entry 信息(找到目标文件后，把它的大小、压缩大小、偏移等信息记录到这里)
 * @param file_name 要查找的文件名：META-INF/MANIFEST.MF
 * @return 0: 找到并填好 entry; 非0: 出错或没找到
 */
static int
find_file(int fd, zentry *entry, const char *file_name) {
    int bytes;
    int res;
    int entry_size;
    int read_size;

    // ZIP 文件第一个 Entry 开始的位置
    // 如果前面有前缀内容（比如可执行壳、自解压等），就可能不是 0
    // ZIP 里所有偏移量都是相对于这个“基准位置”的
    jlong base_offset;

    // 中央目录的起始位置
    jlong censtart;

    // 当前正在处理的中央目录记录的指针（在 buffer 里移动）
    Byte *p;
    // 始终指向 buffer 的起始位置
    Byte *bp;
    // 用来读取中央目录的一大块缓冲区
    Byte *buffer;
    // 用来单独读取某个 Entry 对应的 Local File Header
    Byte locbuf[LOCHDR];

    // 分配用于读取中央目录的大缓冲区
    if ((buffer = (Byte *) malloc(BUFSIZE)) == NULL) {
        return (-1);
    }

    bp = buffer;

    // 定位 ZIP 文件第一个 Entry 的位置(base_offset) 和 中央目录的起始位置(censtart)
    if (find_positions(fd, bp, &base_offset, &censtart) == -1) {
        free(buffer);
        return -1;
    }
    // 把文件读指针移到中央目录的起始处
    if (JLI_Lseek(fd, censtart, SEEK_SET) < (jlong) 0) {
        free(buffer);
        return -1;
    }

    // 先读一小块中央目录进缓冲区
    if ((bytes = read(fd, bp, MINREAD)) < 0) {
        free(buffer);
        return (-1);
    }
    // p 指到缓冲区开始处，准备从第一个中央目录记录开始解析
    p = bp;

    // 遍历每一个中央目录的 header
    // CENSIG_AT: 检查 p 指向的位置是否是一个“中央目录文件头”的签名(0x504B0102)
    while (CENSIG_AT(p)) {
        // bytes 记录读入缓冲区中的字节数

        // 如果读入缓冲区中的数据的长度小于一个完整的中央目录头部的长度(CENHDR)
        // 就用 memmove 把当前未处理的数据(从 p 开始的 bytes 个字节)挪到 buffer 的开头
        // 然后从文件再读一些数据补到后面，确保缓冲区中至少有 CENHDR 这么多字节可用
        if (bytes < CENHDR) {
            p = memmove(bp, p, bytes);
            if ((res = read(fd, bp + bytes, MINREAD)) <= 0) {
                free(buffer);
                return (-1);
            }
            // 更新 bytes
            bytes += res;
        }
        // entry_size = 固定长度(CENHDR) + 三个可变字段总长度
        // - CENNAM(p)：文件名长度
        // - CENEXT(p)：额外字段长度
        // - CENCOM(p)：备注长度
        entry_size = CENHDR + CENNAM(p) + CENEXT(p) + CENCOM(p);
        // 检查当前缓冲区是否容纳了整个中央记录 加上下一个记录的签名(SIGSIZ)
        if (bytes < entry_size + SIGSIZ) {
            if (p != bp)
                p = memmove(bp, p, bytes);
            // 多预读下一个中央记录的签名，是为了下一轮 while (CENSIG_AT(p)) 能正确判断终止条件
            read_size = entry_size - bytes + SIGSIZ;
            read_size = (read_size < MINREAD) ? MINREAD : read_size;
            if ((res = read(fd, bp + bytes, read_size)) <= 0) {
                free(buffer);
                return (-1);
            }
            bytes += res;
        }

        // 判断当前这个 entry 的名字是不是目标文件
        // 1. 首先比较中央记录中的文件名长度是否和 file_name 一样
        // 2. 再用 memcmp 比较字节内容是否相同（字符串完全一致）
        // 如果匹配成功，说明找到了我们想要的 entry（"META-INF/MANIFEST.MF"）
        if ((size_t) CENNAM(p) == JLI_StrLen(file_name) &&
            memcmp((p + CENHDR), file_name, JLI_StrLen(file_name)) == 0) {
            // 找到目标 entry 后，读取它的 Local File Header 并填充信息

            // CENOFF：Local File Header 相对于 base_offset 的偏移
            // 于是 Local Header 的绝对位置就是：base_offset + CENOFF(p)
            if (JLI_Lseek(fd, base_offset + CENOFF(p), SEEK_SET) < (jlong) 0) {
                free(buffer);
                return (-1);
            }
            // 移过去后读出一个 Local Header 到 locbuf
            if (read(fd, locbuf, LOCHDR) < 0) {
                free(buffer);
                return (-1);
            }
            // 检查 Local Header 签名是否正确
            if (!LOCSIG_AT(locbuf)) {
                free(buffer);
                return (-1);
            }
            // 如果都没问题，就开始填充 entry
            entry->isize = CENLEN(p); // 原始文件未压缩的大小
            entry->csize = CENSIZ(p); // 压缩后的大小
            // 真正文件数据（压缩后数据）的起始偏移
            entry->offset = base_offset + CENOFF(p) + LOCHDR +
                            LOCNAM(locbuf) + LOCEXT(locbuf);
            entry->how = CENHOW(p); // 压缩方法
            free(buffer);
            // 返回成功
            return (0);
        }

        // 如果当前 entry 不是目标文件，跳到下一个 entry
        bytes -= entry_size; // 把当前 entry 的总长度从 bytes 中减掉
        p += entry_size; // 指针 p 往后移动一个 entry 的长度，开始解析下一个中央记录
    }
    free(buffer);
    // 整个循环结束都没找到，返回失败
    return (-1);
}
```
