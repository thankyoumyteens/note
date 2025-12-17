# 读取 MANIFEST.MF 文件的内容

```cpp
// --- src/java.base/share/native/libjli/parse_manifest.c --- //

/**
 * 根据 entry，从文件描述符 fd 所指的 zip/jar 文件中，把这个条目对应的内容读出来
 * - 如果是未压缩存储（STORED）：直接读出来返回
 * - 如果是 deflate 压缩（DEFLATED）：用 zlib 解压后返回
 *
 * @param fd JAR 文件的文件描述符
 * @param entry 目标文件的 entry 信息(包括: 原始大小、压缩后的大小、在 jar 包中的偏移位置)
 * @param size_out 如果不为 NULL，会把解压后的大小写进去
 * @return 成功：返回一个 char * 指向内存中的文件内容（额外在末尾加了 '\0'，可以当字符串用）
 *         失败：返回 NULL
 */
static char *
inflate_file(int fd, zentry *entry, int *size_out) {
    // 用来存放从文件中读出的压缩数据（或未压缩数据）
    char *in;
    // 在需要解压时，用来存放解压后的数据
    char *out;
    // zlib 的流结构体，用于解压操作
    z_stream zs;

    // 如果压缩后的大小(csize)或原始大小(isize)是 -1（被当成无效标记），直接认为 entry 无效，返回 NULL。
    if (entry->csize == (size_t) -1 || entry->isize == (size_t) -1) {
        return (NULL);
    }
    // 定位到该 entry 在文件中的位置
    if (JLI_Lseek(fd, entry->offset, SEEK_SET) < (jlong) 0) {
        return (NULL);
    }
    // 分配缓冲区，读取压缩数据
    // 预留 1 字节放 '\0'
    if ((in = malloc(entry->csize + 1)) == NULL) {
        return (NULL);
    }
    // 从文件中读取 csize 字节进 in
    // 如果读到的字节数不等于期望的 csize，说明文件不完整或出错
    if ((size_t) (read(fd, in, (unsigned int) entry->csize)) != entry->csize) {
        free(in);
        return (NULL);
    }
    if (entry->how == STORED) {
        // 情况一：未压缩存储（STORED）

        // 在 in[csize] 的位置写一个 '\0'，方便当 C 字符串使用
        *(char *) ((size_t) in + entry->csize) = '\0';
        // 如果 size_out 不为 NULL，把 csize（即原始大小）写进去
        if (size_out) {
            *size_out = (int) entry->csize;
        }
        // 直接返回 in，调用者拿到的就是文件原始内容
        return (in);
    } else if (entry->how == DEFLATED) {
        // 情况二：DEFLATED 压缩（DEFLATED）

        // 初始化 zlib 解压流
        // 告诉 zlib：
        // 1. 使用默认的内存分配函数（Z_NULL）
        zs.zalloc = (alloc_func) Z_NULL;
        zs.zfree = (free_func) Z_NULL;
        zs.opaque = (voidpf) Z_NULL;
        // 2. 输入数据从 in 开始
        // 3. 输入数据长度为 csize
        zs.next_in = (Byte *) in;
        zs.avail_in = (uInt) entry->csize;
        // 调用 inflateInit2 初始化解压
        // -MAX_WBITS 的用法表示：只解原始 deflate 流，不包含 zlib 或 gzip 头（这是处理 zip 格式时常见的用法）
        if (inflateInit2(&zs, -MAX_WBITS) < 0) {
            free(in);
            return (NULL);
        }
        // 为解压后的数据分配输出缓冲区
        // 再预留 1 字节给 '\0'
        if ((out = malloc(entry->isize + 1)) == NULL) {
            free(in);
            return (NULL);
        }
        // 告诉 zlib 输出写到 out
        zs.next_out = (Byte *) out;
        // 最多写 isize 字节
        zs.avail_out = (uInt) entry->isize;
        // 调用 inflate 执行解压
        if (inflate(&zs, Z_PARTIAL_FLUSH) < 0) {
            free(in);
            free(out);
            return (NULL);
        }
        // 在 out[csize] 的位置写一个 '\0'，方便当 C 字符串使用
        *(char *) ((size_t) out + entry->isize) = '\0';
        // 不再需要 in，释放掉
        free(in);
        // 调用 inflateEnd 清理 zlib 内部资源
        if (inflateEnd(&zs) < 0) {
            free(out);
            return (NULL);
        }
        if (size_out) {
            // 写入解压后的大小 isize
            *size_out = (int) entry->isize;
        }
        return (out);
    }
    free(in);
    return (NULL);
}
```
