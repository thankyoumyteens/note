# 安装前置工具
centos
```
sudo yum install -y wget
sudo yum install -y gcc-c++
sudo yum install -y zlib-devel perl-ExtUtils-MakeMaker
```
ubuntu
```
sudo apt install -y wget
sudo apt install -y gcc-c++
sudo apt install -y zlib-devel perl-ExtUtils-MakeMaker
```

# 下载编译源码
```
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.28.0.tar.gz
tar -zxvf git-2.28.0.tar.gz 
cd git-2.28.0/
./configure --prefix=/usr/local
make
sudo make install
```

# 配置环境变量
```
vim /etc/profile
```
在最后一行添加
```conf
# git
export PATH=$PATH:/usr/local/bin
```
使环境变量生效
```
source /etc/profile
```

# 查看git版本
```
git --version
```
# 初始化git
```
git config --global user.name "Name"
git config --global user.email "email@example.com"
ssh-keygen -t rsa -C "youremail@example.com"
```
