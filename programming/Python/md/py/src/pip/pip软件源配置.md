# pip软件源配置

```
cd ~
mkdir .pip
cd .pip
vim pip.conf
```
配置如下内容: 
```conf
[global]
index-url = https://repo.huaweicloud.com/repository/pypi/simple
trusted-host = repo.huaweicloud.com
timeout = 120
```
