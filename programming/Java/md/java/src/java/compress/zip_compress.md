# zip 压缩

```java
package com.example;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

public class ZipCompressor {


    /**
     * 递归压缩文件到ZipOutputStream
     *
     * @param file      要压缩的文件/目录
     * @param entryName ZIP内部的条目名称（相对路径）
     * @param zos       Zip输出流
     * @throws IOException 处理过程中的IO异常
     */
    private static void compressFile(File file, String entryName, ZipOutputStream zos) throws IOException {
        if (file.isDirectory()) {
            // 如果是目录，添加目录条目（结尾需带"/"）
            if (!entryName.endsWith("/")) {
                entryName += "/";
            }
            zos.putNextEntry(new ZipEntry(entryName));
            zos.closeEntry();

            // 递归压缩子文件/子目录
            File[] children = file.listFiles();
            if (children != null) {
                for (File child : children) {
                    compressFile(child, entryName + child.getName(), zos);
                }
            }
        } else {
            // 如果是文件，直接压缩
            try (FileInputStream fis = new FileInputStream(file)) {
                zos.putNextEntry(new ZipEntry(entryName));

                // 把文件内容写入ZipEntry
                byte[] buffer = new byte[1024 * 8];
                int len;
                while ((len = fis.read(buffer)) != -1) {
                    zos.write(buffer, 0, len);
                }
                // 关闭当前条目
                zos.closeEntry();
            }
        }
    }

    /**
     * 压缩文件或目录到指定ZIP文件
     *
     * @param sourcePath 源文件/目录路径
     * @param zipPath    目标ZIP文件路径（包含文件名）
     * @throws IOException 处理过程中的IO异常
     */
    public static void compress(String sourcePath, String zipPath) throws IOException {
        File sourceFile = new File(sourcePath);
        File zipFile = new File(zipPath);

        // 确保目标目录存在
        if (!zipFile.getParentFile().exists()) {
            var _ = zipFile.getParentFile().mkdirs();
        }

        try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(zipFile))) {
            // 递归处理源文件/目录
            compressFile(sourceFile, sourceFile.getName(), zos);
        }
    }

    // 测试示例
    static void main(String[] args) throws IOException {
        // 压缩单个文件
        compress("a.jpg", "test_single.zip");

        // 压缩目录（包含子文件和子目录）
        compress("testDir", "test_dir.zip");

        System.out.println("压缩完成！");
    }
}
```
