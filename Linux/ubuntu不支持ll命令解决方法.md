# Linux（ubuntu）默认不支持ll命令解决方法
Linux（ubuntu）默认不支持ll命令，必须用ls -l才能查看文件列表信息

解决办法：

1、编辑用户路径下 .bashrc 文件
```
vim ～/.bashrc
```
2、找到#alias ll=‘ls -l’，去掉前面的#
```
alias ll=‘ls -l’
```
保存并退出

3、关闭原来的终端，重启终端命令即可生效
