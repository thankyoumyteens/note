# 创建本地仓库

```java
package com.example;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;

import java.io.File;
import java.io.IOException;

public class App {
    public static void main(String[] args) throws GitAPIException, IOException {
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");
        // 初始化本地仓库
        Git git = Git.init().setDirectory(rootDir).call();
    }
}
```
