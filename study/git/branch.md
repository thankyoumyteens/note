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
