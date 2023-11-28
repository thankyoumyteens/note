# run

推荐的调用子进程的方式是在任何它支持的用例中使用 run() 函数。对于更进阶的用例, 也可以使用底层的 Popen 接口。

run()函数运行 arg 中的指令, 等待指令完成, 然后返回一个 CompletedProcess 实例。

```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None, **other_popen_kwargs)
```

- 如果 capture_output 设为 true, stdout 和 stderr 将会被捕获, 并存储到 CompletedProcess 对象的 stdout 和 stderr 字段中
- cwd 参数指定了子进程的当前目录, args命令都是在这个目录下执行的

## npm 打包

```python
import subprocess

npm_build_cmds = ['C:/Program Files/nodejs/npm.cmd', 'run', 'build']
fe_dir = 'C:/projects/my-vue-app'
r = subprocess.run(npm_build_cmds, shell=False, cwd=fe_dir, capture_output=True)
print(str(r.stdout, encoding="utf-8"))
```
