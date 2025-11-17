# zip 解压

```java
package com.example;

import java.io.*;
import java.nio.file.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ZipDecompressor {

    /**
     * 解压ZIP文件到指定目录
     *
     * @param zipPath ZIP文件路径
     * @param dstDir 目标解压目录
     * @throws IOException 解压过程中的IO异常
     */
    public static void decompress(String zipPath, String dstDir) throws IOException {
        Path zipFilePath = Paths.get(zipPath);
        Path dstDirectory = Paths.get(dstDir);

        // 确保目标目录存在（不存在则创建）
        Files.createDirectories(dstDirectory);

        // 使用try-with-resources自动关闭流
        try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(zipFilePath))) {
            ZipEntry entry;
            // 循环读取ZIP中的每个条目
            while ((entry = zis.getNextEntry()) != null) {
                // 构建目标文件/目录的路径
                Path entryPath = dstDirectory.resolve(entry.getName());

                if (entry.isDirectory()) {
                    // 处理目录：创建对应目录（包括多级目录）
                    Files.createDirectories(entryPath);
                } else {
                    // 处理文件：确保父目录存在，然后写入文件
                    Files.createDirectories(entryPath.getParent()); // 确保父目录存在
                    // 使用NIO的Files.copy高效写入文件
                    Files.copy(zis, entryPath, StandardCopyOption.REPLACE_EXISTING);
                }
                // 关闭当前条目
                zis.closeEntry();
            }
        }
    }

    // 测试示例
    static void main(String[] args) throws IOException {
        decompress("test_dir.zip", "target_dir");
        System.out.println("解压完成！文件已保存到目标目录");
    }
}
```
