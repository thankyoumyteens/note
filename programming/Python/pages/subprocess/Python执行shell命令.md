# Python执行shell命令
```
subprocess.call("touch /rubbish/test1", shell=True)
```
# 执行外部命令并获取它的输出
```python
import subprocess
out_bytes = subprocess.check_output(['netstat','-a'])
out_text = out_bytes.decode('utf-8')
```
如果被执行的命令以非零码返回, 就会抛出异常
```python
try:
    out_bytes = subprocess.check_output(['cmd','arg1','arg2'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output
    code      = e.returncode
```
传递一个字符串参数, 并设置参数shell=True 
```
out_bytes = subprocess.check_output('grep python | wc > out', shell=True)
```
当grep没有匹配到数据时check_output()函数会产生异常
