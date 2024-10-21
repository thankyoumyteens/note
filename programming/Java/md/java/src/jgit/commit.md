# git commit

```java
package com.example;

import org.eclipse.jgit.api.CommitCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.revwalk.RevCommit;

import java.io.File;
import java.io.IOException;

public class App {
    public static void main(String[] args) throws GitAPIException, IOException {
        // git仓库的路径
        File rootDir = new File("/Users/walter/walter/tmp/jgit-demo");

        // 打开git仓库
        Git git = Git.open(rootDir);

        // git commit
        CommitCommand commit = git.commit();
        commit.setMessage("commit 1");
        commit.setCommitter("name", "name@123.com");
        RevCommit call = commit.call();
        String commitId = call.getName();
        System.out.println(commitId);
    }
}
```
