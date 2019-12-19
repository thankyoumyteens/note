# 启动

启动代码格式：`nginx安装目录地址 -c nginx配置文件地址`
```
[root@LinuxServer sbin]# /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
```

# 停止

## 从容停止

查看进程号
```
[root@LinuxServer ~]# ps -ef|grep nginx
```
杀死进程
```
[root@LinuxServer ~]# kill -QUIT 2072
```

## 快速停止

查看进程号
```
[root@LinuxServer ~]# ps -ef|grep nginx
```
杀死进程
```
[root@LinuxServer ~]# kill -TERM 2132
# 或者
[root@LinuxServer ~]# kill -INT 2132
```

## 强制停止
```
[root@LinuxServer ~]# pkill -9 nginx
```

# 重启

## 验证nginx配置文件是否正确

进入nginx安装目录sbin下, 输入命令`./nginx -t`
看到如下显示
```
nginx.conf syntax is ok
nginx.conf test is successful
```
说明配置文件正确

## 重启Nginx服务

进入nginx可执行目录sbin下, 输入命令`./nginx -s reload`即可
