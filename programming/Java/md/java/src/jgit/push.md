# git push

```java
package com.example;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.transport.RefSpec;
import org.eclipse.jgit.transport.SshSessionFactory;
import org.eclipse.jgit.transport.sshd.SshdSessionFactory;

import java.io.File;
import java.io.IOException;

public class App {
    public static void main(String[] args) throws GitAPIException, IOException {
        // 设置私钥
        SshdSessionFactory sshSessionFactory = new SshdSessionFactory();
        sshSessionFactory.setSshDirectory(new File("/Users/walter/.ssh"));
        // 设置认证
        SshSessionFactory.setInstance(sshSessionFactory);

        // git仓库的路径
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");

        // 打开git仓库
        Git git = Git.open(rootDir);

        // git push
        git.push().setRemote("origin").setRefSpecs(new RefSpec("master")).call();
    }
}
```
