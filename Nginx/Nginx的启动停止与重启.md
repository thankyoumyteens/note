# 启动

启动代码格式：`nginx安装目录地址 -c nginx配置文件地址`
```
[root@LinuxServer sbin]# /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
```

# 停止

```
ps -ef|grep nginx
kill -QUIT 2072
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

进入nginx可执行目录sbin下
```
./nginx -s reload
```
