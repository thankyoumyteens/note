# 清空版本记录

1. 
```sh
git checkout master
git checkout --orphan tmp_branch
git add -A && git status
git commit -m "1"
git branch -D master
git branch -m master
git push -f origin master
```
