# Popen

创建并返回一个子进程, 并在这个进程中执行指定的程序: 

```python
subprocess.Popen(args,
    executable=None,
    stdin=None,
    stdout=None,
    stderr=None,
    preexec_fn=None,
    close_fds=False,
    shell=False,
    cwd=None,
    env=None,
    universal_newlines=False,
    startupinfo=None,
    creationflags=0)
```

- args: 要执行的命令或可执行文件的路径。一个由字符串组成的序列(通常是列表), 列表的第一个元素是可执行程序的路径, 剩下的是传给这个程序的参数, 如果没有要传给这个程序的参数, args 参数可以仅仅是一个字符串
- executable: 如果这个参数不是 None, 将替代参数 args 作为可执行程序
- stdin: 指定子进程的标准输入
- stdout: 指定子进程的标准输出
- stderr: 指定子进程的标准错误输出
- 注意: 对于 stdin, stdout 和 stderr 而言, 如果他们是 None(默认情况), 那么子进程使用和父进程相同的标准流文件。父进程如果想要和子进程通过 communicate() 方法通信, 对应的参数必须是 subprocess.PIPE。stdin, stdout 和 stderr 也可以是已经打开的 file 对象, 前提是以合理的方式打开, 比如 stdin 对应的文件必须要可读等。　
- preexec_fn: 默认是None, 否则必须是一个函数或者可调用对象, 在子进程中首先执行这个函数, 然后再去执行为子进程指定的程序或Shell。
- close_fds: 布尔型变量, 为 True 时, 在子进程执行前强制关闭所有除 stdin, stdout和stderr外的文件
- shell: 使用shell运行程序, Python首先起动一个shell, 再用这个shell来解释指定运行的命令。与参数 executable 一同指定子进程运行在什么 Shell 中, 如果executable=None 而 shell=True, 则使用 /bin/sh 来执行 args 指定的程序
- cwd: 指定子进程运行的工作目录, 要求这个目录必须存在
- env: 字典, 键和值都是为子进程定义环境变量的字符串
- universal_newline: 布尔型变量, 为 True 时, stdout 和 stderr 以通用换行(universal newline)模式打开, 
- startupinfo: 见下一个参数
- creationfalgs: 最后这两个参数是Windows中才有的参数, 传递给Win32的CreateProcess API调用。

同 Linux 中创建子进程类似, 父进程创建完子进程后, 并不会自动等待子进程执行。

如果父进程在子进程之前退出, 将导致子进程成为孤儿进程, 孤儿进程统一由 init 进程(Linux下的特殊进程)接管, 负责其终止后的回收工作。

如果父进程在子进程之后终止, 但子进程终止时父进程没有进行最后的回收工作, 子进程残留的数据结构称为僵尸进程。大量僵尸进程将耗费系统资源, 因此父进程及时等待和回收子进程是必要的, 除非能够确认自己比子进程先终止, 从而将回收工作过渡给 init 进程。
