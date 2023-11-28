# 先检查有没有安装ssh服务: 
```
rpm -qa | grep ssh
```

# 如果没有安装ssh服务就安装 :  
```
yum install openssh-server -y
```

# 安装好后在ssh配置文件里进行配置 : 
```
vim /etc/ssh/sshd_config
```

解除Port 22的注释

# 修改完后开启ssh服务
```
systemctl start sshd
```

# 检查ssh服务是否开启
```
ps -e | grep sshd
```

# 检查一下22端口是否开启
```
netstat -an | grep 22
```

# 将ssh服务添加到自启动列表中: 
```
systemctl enable sshd.service
```
