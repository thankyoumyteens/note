# ubuntu软件源配置

备份配置文件：
```
sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
```
修改sources.list文件
```
sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
```
执行apt-get update更新索引
