# 分支操作

## 查看所有分支(包括远程分支)

```sh
git branch -a
```

## 切换到指定远程分支

```sh
# 以远程的dev分支为基础, 新建本地的dev分支
git checkout -b dev origin/dev
```

## 查看本地分支关联的远程分支

```sh
git branch -vv
```

## 删除分支

```sh
git branch -d 本地分支名
git push origin --delete 远程分支名
```
