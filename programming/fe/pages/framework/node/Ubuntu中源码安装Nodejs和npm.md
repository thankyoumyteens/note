# Ubuntu中源码安装Nodejs和npm

更新Ubuntu软件源
```
sudo apt-get update
```
安装python
```
sudo apt-get install python
sudo apt-get install python3
sudo apt-get install python-minimal
```
安装nodejs和npm
```
wget https://repo.huaweicloud.com/nodejs/latest/node-v16.4.0.tar.gz
tar -zxvf node-v16.4.0.tar.gz
cd node-v16.4.0
./configure --prefix=/usr/local/nodejs
make
make install
```
安装完成后测试
```
//查看nodejs安装版本
node -v 
//查看npm安装版本
npm -v 
```
