# 添加远程仓库

```java
package com.example;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.lib.StoredConfig;

import java.io.File;
import java.io.IOException;

public class App {
    public static void main(String[] args) throws GitAPIException, IOException {
        // git仓库的路径
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");

        // 打开git仓库
        Git git = Git.open(rootDir);

        StoredConfig config = git.getRepository().getConfig();
        // 设置远程仓库地址
        String remoteAddr = "git@xxxxx:xxxxx/jgit-demo.git";
        config.setString("remote", "origin", "url", remoteAddr);
        config.save();
    }
}
```
