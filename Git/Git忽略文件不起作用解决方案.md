# Git忽略文件不起作用解决方案

因为gitignore只能忽略那些原来没有被track的文件, 如果某些文件已经纳入版本管理中, 则不会生效。
解决办法就是先把本地缓存删除（改成未track状态）, 然后再提交
```shell
git rm -r --cached .
git add .
git commit -m "update .gitignore"
```
