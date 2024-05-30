# 安装 sudo

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
