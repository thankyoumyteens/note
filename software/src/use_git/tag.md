# 切换到某个 tag

```sh
git checkout tag_name
```

但是，这时候 git 可能会提示你当前处于一个“detached HEAD" 状态。

因为 tag 相当于是一个快照，是不能更改它的代码的。

如果要在 tag 代码的基础上做修改，你需要一个分支：

```sh
git checkout -b branch_name tag_name
```

这样会从 tag 创建一个分支，然后就和普通的 git 操作一样了。
