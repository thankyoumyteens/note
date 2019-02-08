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

# 分支

## git branch: 查看分支列表

```
// *表示当前分支
$ git branch
* master


```

## git checkout -b: 以master为基础创建并切换到新分支

创建分支feature-A
```
$ git checkout -b feature-A
Switched to a new branch 'feature-A'


```
查看分支
```
* feature-A
  master


```
修改index.md, 添加新的一行文本'line2'
```
line1
line2
```
提交修改
```
$ git add index.md
$ git commit -m "add branch"
[feature-A cd9d8a3] add branch
 1 file changed, 1 insertion(+)


```
切换回master分支发现文件并没有被修改
```
$ git checkout master
Switched to branch 'master'

```

切换到work分支可以看到修改后的文件

```
$ git checkout feature-A
Switched to branch 'feature-A'

```

## git checkout -: 切换到上一个分支

```
$ git checkout -
Switched to branch 'master'

$ git checkout -
Switched to branch 'feature-A'

```

## git merge: 合并分支

先切换到master分支
```
$ git checkout master
Switched to branch 'master'
```
将feature-A合并到master中
```
// --no-ff 记录合并到提交历史记录
$ git merge --no-ff feature-A
```
弹出编辑器, 记录提交信息
```
Merge branch 'feature-A'

# Please enter a commit message to explain why this merge is necessary,
# especially if it merges an updated upstream into a topic branch.
#
# Lines starting with '#' will be ignored, and an empty message aborts
# the commit.
~

```

关闭编辑器, 合并完成
```
Merge made by the 'recursive' strategy.
 index.md | 1 +
 1 file changed, 1 insertion(+)


```

## git log --graph: 以图表形式查看日志

```
$ git log --graph
*   commit 2fa975bd69d4ecf57280ad1400482f5b3bc55449 (HEAD -> master)
|\  Merge: 45a9d29 cd9d8a3
| | Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| | Date:   Thu Feb 7 19:52:05 2019 +0800
| |
| |     Merge branch 'feature-A'
| |
| * commit cd9d8a351d33b6fea47e7faf3b771c64fc8abf99 (feature-A)
|/  Author: ZhaoShengZhi <iloveyesterday@outlook.com>
|   Date:   Thu Feb 7 19:50:06 2019 +0800
|
|       add branch
|
* commit 45a9d2976144e2c5a41812a5eaa1bd0bd06f9c43
| Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| Date:   Thu Feb 7 19:45:23 2019 +0800
|
|     add line
|
* commit b18ba4ae033a10590e7049d70a3b224ce2480414
  Author: ZhaoShengZhi <iloveyesterday@outlook.com>
  Date:   Thu Feb 7 19:40:53 2019 +0800

      init


```

# 更改提交的操作

## git reset: 回溯历史版本

回到哈希值指向的时间点所处的状态(创建feature-A分支前的状态)
```
$ git reset --hard 45a9d2976144e2c5a41812a5eaa1bd0bd06f9c43
HEAD is now at 4625ea6 add line


```
创建特性分支fix-B
```
$ git checkout -b fix-B
Switched to a new branch 'fix-B'

```
在index.md中添加一行文本'-fix-B'
```
line1
-fix-B
```
然后提交index.md
```
$ git add index.md

$ git commit -m 'Fix B'
[fix-B 86ea6c2] Fix B
 1 file changed, 1 insertion(+)


```
现在的状态:
```
               *fix-B
              /
             *master
             |
             *
```
接下来回到feature-A合并后的状态:
```
            *master
           /|
 feature-A* |
           \|
            *master
            |
            *
```
由于git log只能查看以当前状态为终点的日志, 所以要使用git reflog查看当前仓库的操作日志
```
$ git reflog
86ea6c2 (HEAD -> fix-B) HEAD@{0}: commit: Fix B
45a9d29 (origin/master, origin/feature-D, master) HEAD@{1}: checkout: moving from feature-D to fix-B
7dbec24 (feature-D) HEAD@{2}: commit: Fix B
45a9d29 (origin/master, origin/feature-D, master) HEAD@{3}: checkout: moving from fix-B to feature-D
45a9d29 (origin/master, origin/feature-D, master) HEAD@{4}: checkout: moving from master to fix-B
45a9d29 (origin/master, origin/feature-D, master) HEAD@{5}: reset: moving to 45a9d2976144e2c5a41812a5eaa1bd0bd06f9c43
2fa975b HEAD@{6}: reset: moving to 2fa975bd69d4ecf57280ad1400482f5b3bc55449
45a9d29 (origin/master, origin/feature-D, master) HEAD@{7}: reset: moving to 45a9d2976144e2c5a41812a5eaa1bd0bd06f9c43
2fa975b HEAD@{8}: merge feature-A: Merge made by the 'recursive' strategy.
45a9d29 (origin/master, origin/feature-D, master) HEAD@{9}: checkout: moving from feature-A to master
cd9d8a3 (feature-A) HEAD@{10}: checkout: moving from feature-A to feature-A
cd9d8a3 (feature-A) HEAD@{11}: commit: add branch
45a9d29 (origin/master, origin/feature-D, master) HEAD@{12}: checkout: moving from master to feature-A
45a9d29 (origin/master, origin/feature-D, master) HEAD@{13}: commit: add line
b18ba4a HEAD@{14}: commit (initial): init


```
找到合并feature-A状态的哈希值2fa975b
```
2fa975b HEAD@{8}: merge feature-A: Merge made by the 'recursive' strategy.
```
恢复状态
```
$ git checkout master
Switched to branch 'master'

$ git reset --hard 2fa975b
HEAD is now at 2fa975b Merge branch 'feature-A'


```
恢复历史后的状态:
```
            *master
           /|
 feature-A* | *fix-B
           \|/
            *master
            |
            *
```
将fix-B合并到master
```
$ git merge --no-ff fix-B
Auto-merging index.md
CONFLICT (content): Merge conflict in index.md
Automatic merge failed; fix conflicts and then commit the result.


```
提示index.md文件发生了冲突(conflict), feature-A修改的部分(line2)与fix-B修改的部分(-fix-B)发生了冲突

## 查看并解决冲突

查看index.md的内容, 变成了这样:
```
line1
<<<<<<< HEAD
line2
=======
-fix-B
>>>>>>> fix-B

```
修改index.md的内容为想要的内容:
```
line1
line2
-fix-B
```
解决冲突后, 执行git add和git commit完成合并
```
$ git add index.md

$ git commit -m "fix conflict"
[master be302d2] fix conflict


```
这样就将fix-B合并到了master分支

## git commit --amend: 修改提交信息

上次的提交信息"fix conflict"实际上是合并fix-B分支的信息
```
$ git log --graph
*   commit be302d2d85ffa245abc7289524cb875107325f3e (HEAD -> master)
|\  Merge: 2fa975b 86ea6c2
| | Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| | Date:   Fri Feb 8 14:42:42 2019 +0800
| |
| |     fix conflict
| |
| * commit 86ea6c25e0f91185789181b7833ac041bae0eede (fix-B)
| | Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| | Date:   Fri Feb 8 14:07:15 2019 +0800
| |
| |     Fix B
| |

```
修改上次提交的信息
```
$ git commit --amend

```
弹出编辑器, 内容如下:
```
fix conflict

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# Date:      Fri Feb 8 14:42:42 2019 +0800
#
# On branch master
# Your branch is ahead of 'origin/master' by 4 commits.
#   (use "git push" to publish your local commits)
#
# Changes to be committed:
#       modified:   index.md
#
~
```
修改内容:
```
Merge branch 'fix-B'

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# Date:      Fri Feb 8 14:42:42 2019 +0800
#
# On branch master
# Your branch is ahead of 'origin/master' by 4 commits.
#   (use "git push" to publish your local commits)
#
# Changes to be committed:
#       modified:   index.md
#
```
保存并关闭编辑器
```
[master 636daba] Merge branch 'fix-B'
 Date: Fri Feb 8 14:42:42 2019 +0800


```
查看提交日志, 提交信息已经修改了
```
$ git log --graph
*   commit 636daba631032d959f5f25cdd07d43d635f708b2 (HEAD -> master)
|\  Merge: 2fa975b 86ea6c2
| | Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| | Date:   Fri Feb 8 14:42:42 2019 +0800
| |
| |     Merge branch 'fix-B'
| |
| * commit 86ea6c25e0f91185789181b7833ac041bae0eede (fix-B)
| | Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| | Date:   Fri Feb 8 14:07:15 2019 +0800
| |
| |     Fix B
| |

```

## git rebase -i: 压缩历史

在合并分支前, 如果发现已经提交的内容有些细小错误, 不妨提交一个修改, 然后将这个修改包含到前一个提交之中, 压缩成一个历史记录

创建分支feature-C
```
$ git checkout -b feature-C
Switched to a new branch 'feature-C'


```
在index.md中添加一行

```
line1
line2
-fix-B
- feattre-C
```
使用git commit -am完成git add和git commit命令
```
$ git commit -am "Add feature-C"
[feature-C 9958573] Add feature-C
 1 file changed, 2 insertions(+), 1 deletion(-)


```
修正刚才的拼写错误
```
line1
line2
-fix-B
- feature-C
```
查看差别
```
$ git diff
diff --git a/index.md b/index.md
index 059a27d..cf2e8ee 100644
--- a/index.md
+++ b/index.md
@@ -1,4 +1,4 @@
 line1
 line2
 -fix-B
-- feattre-C
\ No newline at end of file
+- feature-C
\ No newline at end of file


```
然后提交
```
$ git commit -am "Fix typo"
[feature-C ce01f9f] Fix typo
 1 file changed, 1 insertion(+), 1 deletion(-)


```
将这次提交与上一次提交合并
```
// HEAD代表最新提交
$ git rebase -i HEAD~2

```
弹出编辑器
```
pick 9958573 Add feature-C
pick ce01f9f Fix typo

# Rebase 636daba..ce01f9f onto 636daba (2 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
...
```
将ce01f9f左侧的pick改成fixup
```
pick 9958573 Add feature-C
fixup ce01f9f Fix typo

# Rebase 636daba..ce01f9f onto 636daba (2 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
...
```
保存并关闭编辑器
```
Successfully rebased and updated refs/heads/feature-C.


```
查看提交日志, "Fix typo"已经没有了
```
$ git log --graph
* commit 81c403f84fb28c8e3d43cfebbc720b7a581a0f2b (HEAD -> feature-C)
| Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| Date:   Fri Feb 8 15:09:37 2019 +0800
|
|     Add feature-C
|
*   commit 636daba631032d959f5f25cdd07d43d635f708b2 (master)
|\  Merge: 2fa975b 86ea6c2
| | Author: ZhaoShengZhi <iloveyesterday@outlook.com>
| | Date:   Fri Feb 8 14:42:42 2019 +0800
| |
| |     Merge branch 'fix-B'
| |

```
将feature-C合并到master
```
$ git checkout master
Switched to branch 'master'

$ git merge --no-ff feature-C
Merge made by the 'recursive' strategy.
 index.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)


```

# 推送至远程仓库

## git remote add: 添加远程仓库

将https://gitee.com/thankyoumyteens/git-study.git远程仓库的名称设置为origin
```
$ git remote add origin https://gitee.com/thankyoumyteens/git-study.git

```

## git push: 推送至远程仓库

推送到远程分支

-u参数在推送的同时将origin仓库的master分支设置为本地仓库当前分支的upstream, 将来git pull时这个分支可以直接从origin的master分支获取内容, 不必加额外的参数
```
$ git push -u origin master
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 4 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (6/6), 440 bytes | 110.00 KiB/s, done.
Total 6 (delta 0), reused 0 (delta 0)
remote: Powered By Gitee.com
To https://gitee.com/thankyoumyteens/git-study.git
 + 0eaeffd...45a9d29 master -> master (forced update)
Branch 'master' set up to track remote branch 'master' from 'origin'.


```
推送到master以外的分支

创建feature-D分支
```
$ git checkout -b feature-D
Switched to a new branch 'feature-D'


```
将它推送到远程仓库
```
$ git push -u origin feature-D
Total 0 (delta 0), reused 0 (delta 0)
remote: Powered By Gitee.com
To https://gitee.com/thankyoumyteens/git-study.git
 * [new branch]      feature-D -> feature-D
Branch 'feature-D' set up to track remote branch 'feature-D' from 'origin'.


```
这样在远程仓库也创建了分支feature-D

# 从远程仓库获取

## git clone: 获取远程仓库

执行git clone后悔默认处于master分支下, 同时系统会自动将origin设置成该远程仓库的标识符
```
$ git clone https://gitee.com/thankyoumyteens/git-study.git
Cloning into 'git-study'...
remote: Enumerating objects: 20, done.
remote: Counting objects: 100% (20/20), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 20 (delta 3), reused 0 (delta 0)
Unpacking objects: 100% (20/20), done.


```
查看当前分支相关信息

-a参数可以同时显示本地仓库和远程仓库的分支信息
```
$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/feature-D
  remotes/origin/master


```

## 获取远程分支

将远程的feature-D获取到本地仓库

```
// 以远程的feature-D分支为来源, 
// 在本地仓库创建feature-D分支
$ git checkout -b feature-D origin/feature-D
Switched to a new branch 'feature-D'
Branch 'feature-D' set up to track remote branch 'feature-D' from 'origin'.


```
向本地的feature-D分支提交更改
```
line1
-feature-D
```
```
$ git commit -am "Add feature-D"
[feature-D dc31e1d] Add feature-D
 1 file changed, 1 insertion(+)


```
推送feature-D分支
```
$ git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (3/3), 271 bytes | 135.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
remote: Powered By Gitee.com
To https://gitee.com/thankyoumyteens/git-study.git
   45a9d29..dc31e1d  feature-D -> feature-D


```

## git pull: 获取最新的远程仓库分支

```
$ git pull origin feature-D
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (3/3), done.
From https://gitee.com/thankyoumyteens/git-study
 * branch            feature-D  -> FETCH_HEAD
   45a9d29..dc31e1d  feature-D  -> origin/feature-D
Auto-merging index.md
CONFLICT (content): Merge conflict in index.md
Automatic merge failed; fix conflicts and then commit the result.


```
