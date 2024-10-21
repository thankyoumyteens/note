# git add

```java
package com.example;

import org.eclipse.jgit.api.AddCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.dircache.DirCache;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class App {
    public static void main(String[] args) throws GitAPIException, IOException {
        // git仓库的路径
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");

        // 创建新文件
        Path root = Paths.get(rootDir.getAbsolutePath());
        Path path = root.resolve("1.txt");
        Files.write(path, "111".getBytes());

        // 打开git仓库
        Git git = Git.open(rootDir);

        // git add
        AddCommand add = git.add();
        // 需要使用相对路径
        String relativePath = root.relativize(path).toString();
        add.addFilepattern(relativePath);
        DirCache call = add.call();
        System.out.println(call);
    }
}
```
