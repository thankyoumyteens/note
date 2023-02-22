# subprocess模块定义的异常
```python
exception subprocess.CalledProcessError
```
什么时候可能抛出该异常：调用 check_call() 或 check_output() ，子进程的退出状态不为 0 时。

该异常包含以下信息：

1. returncode：子进程的退出状态；
2. cmd：创建子进程时指定的命令；
3. output：如果是调用 check_output() 时抛出的该异常，这里包含子进程的输出，否则该属性为None。
 