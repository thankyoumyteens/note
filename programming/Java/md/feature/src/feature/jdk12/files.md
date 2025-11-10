# Files 类增强

Java 12 对 java.nio.file.Files 类引入了一项主要增强：mismatch 方法（JEP 325: Update the java.nio.file Package with New Features）。这项改进旨在提升文件内容的比较效率，尤其适用于大型二进制文件，而无需将整个文件加载到内存中。其他文件操作（如读取/写入字符串）主要在 Java 11 中引入，Java 12 未有进一步的字符串相关文件增强。

```java
public static long mismatch(Path path, Path path2) throws IOException
```

比较两个文件的内容，返回第一个不匹配字节的位置（从 0 开始计数）。如果文件完全匹配（包括大小相同且所有字节相同），返回 `-1L`。如果文件大小不同但前缀匹配，则返回较小文件的大小。

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

Path path1 = Paths.get("file1.txt");
Path path2 = Paths.get("file2.txt");
try {
    long mismatchPos = Files.mismatch(path1, path2);
    if (mismatchPos == -1L) {
        System.out.println("文件完全匹配。");
    } else {
        System.out.println("第一个不匹配字节位置: " + mismatchPos);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```
