# 如何将某一个分支的部分代码合并到另外一个分支上面

需求：在A分支上面开发了一个功能，突然B分支说也需要这个功能，但是不想要合并A分支上所有的代码；只需要合并这一个功能对应的代码

在A分支上通过`git log` 查看日志；找到commit对应的hash值，如：b5dc0dd

切换到分支B `git checkout B`

通过`git cherry-pick commit对应的hash值`将当前hash对应提交的代码合并到B分支上去: `git cherry-pick b5dc0dd`
