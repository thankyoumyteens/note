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
