# 安装前置工具

```
sudo apt install -y wget gcc g++ zlib1g.dev tcl build-essential tk gettext
```

# 卸载旧版本

```
sudo apt remove git
```

# 下载编译源码

```
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.42.0.tar.gz
tar -zxvf git-2.42.0.tar.gz 
cd git-2.42.0/
./configure --prefix=/usr/local
make
sudo make install
```

# 配置环境变量

1. 打开配置文件
```
sudo vim /etc/profile
```

2. 在最后一行添加：
```conf
# git
export PATH=$PATH:/usr/local/bin
```

3. 使环境变量生效
```
source /etc/profile
```

# 查看git版本

```
git --version
```

# 初始化git

```
git config --global user.name "zhaosz"
git config --global user.email "iloveyesterday@outlook.com"
ssh-keygen -t rsa -C "iloveyesterday@outlook.com"
```
