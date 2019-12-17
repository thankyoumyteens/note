# Python执行shell命令

`subprocess.call("touch /rubbish/test1", shell=True)`

# 执行外部命令并获取它的输出

使用 `subprocess.check_output()` 函数。例如: 
```
import subprocess
out_bytes = subprocess.check_output(['netstat','-a'])
```
这段代码执行一个指定的命令并将执行结果以一个字节字符串的形式返回。 如果你需要文本形式返回, 加一个解码步骤即可。例如: 
```
out_text = out_bytes.decode('utf-8')
```
如果被执行的命令以非零码返回, 就会抛出异常。 下面的例子捕获到错误并获取返回码: 
```
try:
    out_bytes = subprocess.check_output(['cmd','arg1','arg2'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    code      = e.returncode   # Return code
```
通常来讲, 命令的执行不需要使用到底层shell环境(比如sh、bash)。 一个字符串列表会被传递给一个低级系统命令, 比如 `os.execve()` 。 如果你想让命令被一个shell执行, 传递一个字符串参数, 并设置参数 `shell=True`, 有时候你想要Python去执行一个复杂的shell命令的时候这个就很有用了, 比如管道流, I/O重定向和其他特性。例如: 
```
out_bytes = subprocess.check_output('grep python | wc > out', shell=True)
```

# grep

grep命令的返回值: 
* `0` 匹配到行
* `1` 没有匹配
* `>1` 发生错误

所以当grep没有匹配到数据时`subprocess.check_output()`函数会产生异常
