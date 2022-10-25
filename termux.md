# 替换为国内镜像

```
sed -i 's@^\(deb.*stable main\)$@#\1\ndeb https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main stable main@' $PREFIX/etc/apt/sources.list
apt update && apt upgrade
```

# 常用软件

```
apt update
apt upgrade
apt install python
apt install clang
apt install git
apt install vim
```

# 访问手机内置存储

```
termux-setup-storage
```

# 开启ssh

### termux开启的sshd服务用的是8022端口，而不是常用的22端口
```
apt install openssh
sshd
```

### 查看ip
```
ifconfig
```

### 查看用户名
```
whoami
```

### 设置密码
```
passwd
```

### 设置自动开启ssh
```
echo "sshd" >> ~/.bashrc
```
