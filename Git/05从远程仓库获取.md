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
