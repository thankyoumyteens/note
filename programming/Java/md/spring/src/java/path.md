# 路径操作

创建 Path:

```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class App {
    public static void main(String[] args) {
        Path path = Paths.get("/home");
        System.out.println(path);
    }
}
```

## 获取当前 class 文件所在的路径

```java
String path = this.getClass().getResource("").getPath();
```

## 获取当前当前登录用户的家路径

```java
String homePath = System.getProperty("user.home");
```

## 获取当前工作目录

```java
String workPath = System.getProperty("user.dir");
```

## 获取绝对路径

```java
// 传入相对路径(相对于工作目录)
Path path = Paths.get("a.txt");
// 获取绝对路径
path = path.toAbsolutePath();
```

## 获取相对路径

```java
// 传入绝对路径
Path absolutePath = Paths.get("/home/demo/a.txt");
// 获取相对/home/demo的路径: a.txt
Path dirPath = Paths.get("/home/demo");
Path relativePath = dirPath.relativize(absolutePath);
```

## 拼接路径

```java
Path dirPath = Paths.get("/home/demo");
// /home/demo/a.txt
Path path = dirPath.resolve("a.txt");
```

## 拆分路径

```java
Path path = Paths.get("/home/demo/a.txt");
// home
// demo
// a.txt
for (int i = 0; i < path.getNameCount(); i++) {
    Path name = path.getName(i);
    System.out.println(name);
}
```

## 获取上级目录/文件名/扩展名

```java
Path path = Paths.get("/home/demo/a.txt");
// /home/demo
Path parent = path.getParent();
// a.txt
Path fileName = path.getFileName();
// .txt
String ext = fileName.toString().substring(fileName.toString().lastIndexOf("."));
```

## 遍历目录下所有文件和文件夹

```java
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;

public class App {

    public static void main(String[] args) {
        Path path = Paths.get("/home/demo");
        // 递归遍历
        Files.walkFileTree(path, new FileVisitor<Path>() {

            /**
             * 访问文件夹之前自动调用此方法
             */
            @Override
            public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
                System.out.println("当前访问的目录：" + dir);
                return FileVisitResult.CONTINUE;
            }

            /**
             * 访问文件时自动调用此方法
             */
            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                System.out.println("当前访问的文件：" + file);
                return FileVisitResult.CONTINUE;
            }

            /**
             * 访问文件失败时自动调用此方法
             */
            @Override
            public FileVisitResult visitFileFailed(Path file, IOException exc) {
                System.out.println("访问文件失败：" + file);
                return FileVisitResult.TERMINATE;
            }

            /**
             * 访问文件夹之后自动调用此方法
             */
            @Override
            public FileVisitResult postVisitDirectory(Path dir, IOException exc) {
                System.out.println("访问文件夹结束：" + dir);
                return FileVisitResult.CONTINUE;
            }
        });
    }
}
```

## 创建多级文件夹

```java
Path path = Paths.get("/home/demo/a/b/c");
Files.createDirectories(path);
```

## 复制文件

```java
Path dir = Paths.get("/home/demo_dir");
Path src = dir.resolve("1.txt");
Path dest = dir.resolve("2.txt");
// 复制文件
// COPY_ATTRIBUTES: 复制文件属性(创建时间, 修改时间等)
// REPLACE_EXISTING: 如果目标文件存在则替换
Files.copy(src, dest, StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
```

## 复制文件夹

```java
Path srcDir = Paths.get("/home/demo_dir");
Path destDir = Paths.get("/home/copied_demo_dir");
// 递归复制
Files.walkFileTree(srcDir, new SimpleFileVisitor<Path>() {
    /**
     * 复制文件夹
     */
    @Override
    public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
        Path relativePath = srcDir.relativize(dir);
        Path targetDir = destDir.resolve(relativePath);
        try {
            Files.copy(dir, targetDir);
        } catch (FileAlreadyExistsException e) {
            // ignore
        }
        return FileVisitResult.CONTINUE;
    }

    /**
     * 复制文件
     */
    @Override
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
        Path relativePath = srcDir.relativize(file);
        Files.copy(file, destDir.resolve(relativePath));
        return FileVisitResult.CONTINUE;
    }
});
```

## 移动文件

```java
Path dir = Paths.get("/home/demo_dir");
Path src = dir.resolve("1.txt");
Path dest = dir.resolve("2.txt");
// 移动文件
// REPLACE_EXISTING: 如果目标文件存在则替换
Files.move(src, dest, StandardCopyOption.REPLACE_EXISTING);
```

## 删除文件

```java
Path path = Paths.get("/home/demo/a.txt");
Files.deleteIfExists(path);
```
