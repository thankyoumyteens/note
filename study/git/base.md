# 基本操作

## git init: 初始化仓库

```
$ git init
Initialized empty Git repository in /git-study/.git/
```

## git status: 查看仓库状态

```
$ git status
// 当前处于master分支
On branch master

// 还没有提交
No commits yet

// 没有要提交的内容
nothing to commit (create/copy files and use "git add" to track)

```
创建文件
```
$ touch index.md
```
再查看仓库状态
```
$ git status
On branch master

No commits yet

// 还没有被git管理的文件
Untracked files:
  (use "git add <file>..." to include in what will be committed)

        index.md

nothing added to commit but untracked files present (use "git add" to track)

```

## git add: 向暂存区添加文件

暂存区是提交之前的临时区域

将index.md加入暂存区
```
$ git add index.md
```
再查看仓库状态
```
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   index.md
```

## git commit: 将暂存区中的文件保存到仓库的历史记录

```
// -m 参数表示提交信息(这次提交的说明)
// 不加参数-m会启动编辑器编辑更加详细的信息
$ git commit -m "init"
[master (root-commit) b18ba4a] init
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 index.md

```
提交后查看状态
```
$ git status
On branch master
nothing to commit, working tree clean

```

## git log: 查看提交日志

```
$ git log
// 指向这次提交的哈希值
commit b18ba4ae033a10590e7049d70a3b224ce2480414 (HEAD -> master)
// 提交人
Author: zhaoshengzhi <iloveyesterday@outlook.com>
// 提交时间
Date:   Sun Sep 2 14:52:58 2018 +0800

// 提交信息
    init


```

## git diff: 查看更改前后的差别

修改index.md, 添加一行文本'line1'
```
line1
```
使用git diff查看当前工作树与暂存区的区别
```
// '+'表示增加的内容
// '-'表示删除的内容
$ git diff
diff --git a/index.md b/index.md
index e69de29..a29bdeb 100644
--- a/index.md
+++ b/index.md
@@ -0,0 +1 @@
+line1

```
将index.md加入暂存区
```
$ git add index.md
```
再次查看区别
```
// 当前工作树与暂存区没有区别, git diff无结果
$ git diff

```
再查看两次提交的区别
```
//HEAD指向当前分支中最新一次提交
$ git diff HEAD
diff --git a/index.md b/index.md
index e69de29..a29bdeb 100644
--- a/index.md
+++ b/index.md
@@ -0,0 +1 @@
+line1

```
提交修改
```
$ git commit -m "add line"
[master 45a9d29] add line
 1 file changed, 1 insertion(+)

```
查看日志
```
$ git log
commit 45a9d2976144e2c5a41812a5eaa1bd0bd06f9c43 (HEAD -> master)
Author: ZhaoShengZhi <iloveyesterday@outlook.com>
Date:   Thu Feb 7 19:45:23 2019 +0800

    add line

commit b18ba4ae033a10590e7049d70a3b224ce2480414
Author: ZhaoShengZhi <iloveyesterday@outlook.com>
Date:   Thu Feb 7 19:40:53 2019 +0800

    init

```
