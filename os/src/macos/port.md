# 端口占用

```sh
lsof -i tcp:端口号
```

在输出中找到进程的 pid

```sh
kill -9 pid
```
