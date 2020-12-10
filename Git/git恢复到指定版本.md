# git恢复到指定版本

查看git的提交版本和id 拿到需要恢复的版本号 
```
git log　 
```
恢复到指定版本 
```
//后面这一大串就是版本id
git reset --hard 44f994dd8fc1e10c9ed557824cae50d1586d0cb3
```
强制push
```
git push -f origin master
```
