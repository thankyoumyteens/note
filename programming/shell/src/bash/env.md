# 环境变量

环境变量是 Bash 环境自带的变量, 进入 Shell 时已经定义好了, 可以直接使用。

```sh
# 显示所有环境变量
$ env

# 查看单个环境变量的值
$ echo $PATH
```

## 常见的环境变量

- BASHPID: Bash 进程的进程 ID
- BASHOPTS: 当前 Shell 的参数, 可以用 shopt 命令修改
- DISPLAY: 图形环境的显示器名字, 通常是:0, 表示 X Server 的第一个显示器
- EDITOR: 默认的文本编辑器
- HOME: 用户的主目录
- HOST: 当前主机的名称
- IFS: 词与词之间的分隔符, 默认为空格
- LANG: 字符集以及语言编码, 比如 zh_CN.UTF-8
- PATH: 由冒号分开的目录列表, 当输入可执行程序名后, 会搜索这个目录列表
- PS1: Shell 提示符
- PS2:  输入多行命令时, 次要的 Shell 提示符
- PWD: 当前工作目录
- RANDOM: 返回一个 0 到 32767 之间的随机数
- SHELL: Shell 的名字
- SHELLOPTS: 启动当前 Shell 的 set 命令的参数
- TERM: 终端类型名, 即终端仿真器所用的协议
- UID: 当前用户的 ID 编号
- USER: 当前用户的用户名
