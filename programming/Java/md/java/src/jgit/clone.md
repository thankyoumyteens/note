# git clone

```java
package com.example;

import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.transport.SshSessionFactory;
import org.eclipse.jgit.transport.sshd.SshdSessionFactory;

import java.io.File;

public class App {
    public static void main(String[] args) throws GitAPIException {
        // 设置私钥
        SshdSessionFactory sshSessionFactory = new SshdSessionFactory();
        sshSessionFactory.setSshDirectory(new File("/Users/walter/.ssh"));
        // 设置认证
        SshSessionFactory.setInstance(sshSessionFactory);
        
        // 要克隆到的路径
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");

        // 远程仓库地址
        String remoteAddr = "git@xxxxx:xxxxx/jgit-demo.git";

        // git clone
        Git git = Git.cloneRepository().setURI(remoteAddr).setDirectory(rootDir).call();
    }
}
```
