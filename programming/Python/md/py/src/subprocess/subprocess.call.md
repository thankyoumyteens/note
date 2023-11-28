# subprocess.call
```python
subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
```
父进程直接创建子进程执行程序, 然后等待子进程完成

返回值: call() 返回子进程的 退出状态 即 child.returncode 属性；

# subprocess.check_call
```python
subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
```
父进程直接创建子进程执行程序, 然后等待子进程完成, 具体可以使用的参数, 参考上文 Popen 类的介绍。

返回值: 无论子进程是否成功, 该函数都返回 0

如果子进程的退出状态不是0, check_call() 抛出异常 CalledProcessError, 异常对象中包含了 child.returncode 对应的返回码。

