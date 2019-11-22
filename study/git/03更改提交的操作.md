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
