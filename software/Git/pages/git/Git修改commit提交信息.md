# 修改最后一次提交信息

有些时候不小心git commit -m ‘提交信息’中的提交信息写错了。

执行如下命令即可修改

注意，仅仅只能针对最后一次提交

```
git commit --amend -m "新的修改提交信息"
```

# 修改任意一次提交信息

查看提交日志
```
git log
```

变基操作
```
git rebase -i <commit range>
```
可以用`commit~n`或`commit^^`这种形式替代：前者表示当前提交到n次以前的提交，后者`^`符号越多表示的范围越大，commit可以是`HEAD`或者某次提交的hash值；`-i`参数表示进入交互模式。

如修改最近3次的信息:
```
git rebase -i HEAD~3
```

在弹出的窗口中，以VIM编辑方式显示了最近3次的提交信息。将想要修改的提交前的pick改为edit，如果需要修改多个，也可以将对应的多个pick改为edit

修改完保存退出

修改commit信息
```
git commit --amend
```
然后会弹出新的窗口，在弹出的窗口中，就可以修改commit信息了。如果修改了多个pick为edit，则会多次弹出修改界面

修改完保存退出

完成变基操作
```
git rebase --continue
```
有时候会完成变基失败，需要`git add --all`才能解决，一般git会给出提示。

查看提交日志，对比变基前后的修改
```
git log
```

推送到远程
```
git push
```
