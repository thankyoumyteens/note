# 基本使用

1. 依赖

```xml
<dependency>
    <groupId>org.eclipse.jgit</groupId>
    <artifactId>org.eclipse.jgit</artifactId>
    <version>7.0.0.202409031743-r</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jgit</groupId>
    <artifactId>org.eclipse.jgit.ssh.apache</artifactId>
    <version>7.0.0.202409031743-r</version>
</dependency>
```

2. 使用

```java
package com.example;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.lib.StoredConfig;
import org.eclipse.jgit.transport.RefSpec;
import org.eclipse.jgit.transport.SshSessionFactory;
import org.eclipse.jgit.transport.sshd.SshdSessionFactory;

import java.io.File;
import java.io.IOException;

public class App {
    public static void main(String[] args) throws GitAPIException, IOException {
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");
        // 初始化本地仓库
        Git git = Git.init().setDirectory(rootDir).call();

        StoredConfig config = git.getRepository().getConfig();
        // 设置远程仓库地址
        String remoteAddr = "git@xxxxx:xxxxx/jgit-demo.git";
        config.setString("remote", "origin", "url", remoteAddr);
        config.save();

        // 添加文件
        File file = new File(rootDir, "README.md");
        file.createNewFile();
        git.add().addFilepattern("README.md").call();

        // 提交
        git.commit().setMessage("Initial commit").call();

        // 设置私钥
        SshdSessionFactory sshSessionFactory = new SshdSessionFactory();
        sshSessionFactory.setSshDirectory(new File("/demo/.ssh"));

        // 设置认证
        SshSessionFactory.setInstance(sshSessionFactory);

        // 推送
        git.push().setRemote("origin").setRefSpecs(new RefSpec("master")).call();
    }
}
```
