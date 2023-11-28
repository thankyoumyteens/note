# subprocess.check_output
```python
subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False)
```
父进程直接创建子进程执行程序, 以字符串的形式返回子进程的输出。

返回值: 字符串形式的子进程的输出结果

如果子进程的 退出状态 不是0, 那么抛出异常 CalledProcessError, 异常对象中包含了 child.returncode 对应的返回码。

注意: check_output() 的函数定义中没有参数 stdout, 调用该方法时, 子进程的输出默认就返回给父进程。
