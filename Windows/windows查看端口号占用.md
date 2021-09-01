# windows查看端口号占用

```
netstat -ano|findstr "80"
```

输出的最后一列的6532为PID号，根据这个PID号继续找相对应的进程

```
tasklist|findstr "6532"
```

输出进程名，找到任务管理器，结束这个进程


或者用命令直接结束这个进程

```
tskill 6532
````
