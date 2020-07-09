# ssh 登陆进去后 .bashrc 也没有被执行
## 原因
ssh在login之后, 会执行.bash_profile文件
## 解决
新建一个.bash_profile,内容如下
```
if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
```
