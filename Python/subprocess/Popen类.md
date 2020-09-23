# 构造方法

创建并返回一个子进程, 并在这个进程中执行指定的程序。
```python
subprocess.Popen(args, 
    bufsize=0, 
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

# 参数介绍: 

- args: 要执行的命令或可执行文件的路径。一个由字符串组成的序列(通常是列表), 列表的第一个元素是可执行程序的路径, 剩下的是传给这个程序的参数, 如果没有要传给这个程序的参数, args 参数可以仅仅是一个字符串。
- bufsize: 控制 stdin, stdout, stderr 等参数指定的文件的缓冲, 和打开文件的 open()函数中的参数 bufsize 含义相同。
- executable: 如果这个参数不是 None, 将替代参数 args 作为可执行程序
- stdin: 指定子进程的标准输入
- stdout: 指定子进程的标准输出
- stderr: 指定子进程的标准错误输出
- 注意: 对于 stdin, stdout 和 stderr 而言, 如果他们是 None（默认情况）, 那么子进程使用和父进程相同的标准流文件。父进程如果想要和子进程通过 communicate() 方法通信, 对应的参数必须是 subprocess.PIPE。stdin, stdout 和 stderr 也可以是已经打开的 file 对象, 前提是以合理的方式打开, 比如 stdin 对应的文件必须要可读等。　
- preexec_fn: 默认是None, 否则必须是一个函数或者可调用对象, 在子进程中首先执行这个函数, 然后再去执行为子进程指定的程序或Shell。
- close_fds: 布尔型变量, 为 True 时, 在子进程执行前强制关闭所有除 stdin, stdout和stderr外的文件
- shell: 布尔型变量, 明确要求使用shell运行程序, 与参数 executable 一同指定子进程运行在什么 Shell 中, 如果executable=None 而 shell=True, 则使用 /bin/sh 来执行 args 指定的程序也就是说, Python首先起一个shell, 再用这个shell来解释指定运行的命令。
- cwd: 代表路径的字符串, 指定子进程运行的工作目录, 要求这个目录必须存在
- env: 字典, 键和值都是为子进程定义环境变量的字符串
- universal_newline: 布尔型变量, 为 True 时, stdout 和 stderr 以通用换行（universal newline）模式打开, 
- startupinfo: 见下一个参数
- creationfalgs: 最后这两个参数是Windows中才有的参数, 传递给Win32的CreateProcess API调用。

同 Linux 中创建子进程类似，父进程创建完子进程后，并不会自动等待子进程执行。

如果父进程在子进程之前退出, 将导致子进程成为孤儿进程，孤儿进程统一由 init 进程(Linux下的特殊进程)接管，负责其终止后的回收工作。

如果父进程在子进程之后终止，但子进程终止时父进程没有进行最后的回收工作，子进程残留的数据结构称为僵尸进程。大量僵尸进程将耗费系统资源，因此父进程及时等待和回收子进程是必要的，除非能够确认自己比子进程先终止，从而将回收工作过渡给 init 进程。

# Popen 对象的属性

## pid
子进程的PID。

## returncode
该属性表示子进程的返回状态，returncode可能有多重情况：

1. None: 子进程尚未结束；
2. 0: 子进程正常退出；
3. 大于 0: 子进程异常退出，returncode对应于出错码；
4. 小于 0: 子进程被信号杀掉了。

## stdin, stdout, stderr
子进程对应的一些初始文件，如果调用Popen()的时候对应的参数是subprocess.PIPE，则这里对应的属性是一个包裹了这个管道的 file 对象

# Popen 对象的方法

## poll()
检查子进程  p 是否已经终止，返回 p.returncode 属性

## wait()
等待子进程 p 终止，返回 p.returncode 属性；

注意: wait() 立即阻塞父进程，直到子进程结束

## communicate(input=None)
和子进程 p 交流，将参数 input 中的数据发送到子进程的 stdin，同时从子进程的 stdout 和 stderr 读取数据，直到EOF。

返回值: 二元组 (stdoutdata, stderrdata) 分别表示从标准输出和标准错误中读出的数据。

父进程调用 p.communicate() 和子进程通信有以下限制：

1. 只能通过管道和子进程通信，也就是说，只有调用 Popen() 创建子进程的时候参数 stdin=subprocess.PIPE，才能通过 p.communicate(input) 向子进程的 stdin 发送数据；只有参数 stout 和 stderr 也都为 subprocess.PIPE ，才能通过p.communicate() 从子进程接收数据，否则接收到的二元组中，对应的位置是None。
2. 父进程从子进程读到的数据缓存在内存中，因此commucate()不适合与子进程交换过大的数据。

注意: communicate() 立即阻塞父进程，直到子进程结束

## send_signal(signal)
向子进程发送信号 signal

## terminate()
终止子进程 p ，等于向子进程发送 SIGTERM 信号

## kill()
杀死子进程 p ，等于向子进程发送 SIGKILL 信号

