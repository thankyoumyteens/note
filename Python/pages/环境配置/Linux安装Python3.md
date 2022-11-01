# CentOS安装Python3
安装编译相关的包
```
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel
wget https://repo.huaweicloud.com/python/3.7.9/Python-3.7.9.tgz
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

# Ubuntu安装Python3

```
sudo apt-get install -y zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev
wget https://repo.huaweicloud.com/python/3.7.9/Python-3.7.9.tgz
tar -zxvf Python-3.7.9.tgz
cd Python-3.7.9
./configure prefix=/usr/local/python3 
sudo make
sudo make install
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3
python3 -V
```
