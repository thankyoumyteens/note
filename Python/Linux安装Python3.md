# Linux安装Python3
安装编译相关的包
```
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel
```
安装pip
```
yum -y install epel-release 
yum install python-pip
```
安装一下 wget
```
pip install wget
```
下载 python3.7的源码
```
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar -zxvf Python-3.7.0.tgz
./configure prefix=/usr/local/python3 
make && make install
```
添加软链接
```
#添加python3的软链接
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3 
#添加 pip3 的软链接 
ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3
#测试是否安装成功了 
python3 -V
```
