# 查看ssh服务是否开启

```
sudo ps -e | grep ssh
```

# 安装ssh服务端程序

```
sudo apt-get install openssh-server
```

# 安装ssh客户端程序

```
sudo apt-get install openssh-client
```

# 允许密码登录

```
sudo vim /etc/ssh/sshd_config
```

- 搜索关键字 PasswordAuthentication
- 将PasswordAuthentication no 改为 yes
- 保存文件

# 开启ssh服务

```
sudo /etc/init.d/ssh start
```

# 关闭ssh服务

```
sudo /etc/init.d/ssh stop
```

# 开机自动启动ssh


```
sudo systemctl enable ssh
```

# 关闭ssh开机自动启动

```
sudo systemctl disable ssh
```
