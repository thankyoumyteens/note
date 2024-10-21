# 设置 ssh 认证

```java
package com.example;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
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
    }
}
```
