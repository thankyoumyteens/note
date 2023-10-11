# git基于某个分支创建分支

1、拷贝源代码
```
git clone git@git地址 
```

2、根据已有分支创建新的分支
```
git checkout -b yourbranchname origin/oldbranchname
```

- -b: 创建并且切换到该分支

3、推送到git
```
git push origin yourbranchname 
```
