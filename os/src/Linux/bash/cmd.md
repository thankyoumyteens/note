# Shell 命令

Shell 命令的格式:

```sh
command [ arg1 ... [ argN ]]
```

同一个参数一般有长和短两种形式, 比如 `ls -a` 的 -a 是短形式, `ls --all` 的 --all 是长形式, 它们的作用完全相同。短形式便于手动输入, 长形式一般用在脚本之中, 可读性更好。

## 多行命令

有些命令比较长, 写成多行会有利于阅读和编辑, 多行命令需要使用反斜杠 `\` 进行连接:

```sh
$ echo \
> -e \
> "line1\nline2"
line1
line2
```

## 连接多个命令

- && 表示前一条命令执行成功时, 才执行后一条命令
- || 表示上一条命令执行失败时, 才执行下一条命令
- ; 表示不管上一条命令是否执行成功, 都会执行下一条命令

```sh
$ mkdir test/1/2/3 && echo "success"
mkdir: cannot create directory ‘test/1/2/3’: No such file or directory

$ mkdir test/1/2/3 || echo "success"
mkdir: cannot create directory ‘test/1/2/3’: No such file or directory
success

$ mkdir test/1/2/3 ; echo "success"
mkdir: cannot create directory ‘test/1/2/3’: No such file or directory
success
```
