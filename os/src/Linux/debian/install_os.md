# 安装 debian

![](../img/1.png)
![](../img/2.png)
![](../img/3.png)
![](../img/4.png)
![](../img/5.png)

## 安装 sudo

```sh
# 使用root账号
su
apt-get install sudo
apt-get install vim -y

vim /etc/sudoers
# 在%sudo ALL=(ALL:ALL) ALL 这一行底下加入: 
# 用户名 ALL=(ALL) ALL
# 保存退出vim

# 退出root
exit
```

## 连接 ssh

启动 ssh:

```sh
sdo systemctl start ssh.service
# 查看ip地址
ip address
```

连接 ssh:

- 端口 -> 22
- 用户 -> 非 root 用户
