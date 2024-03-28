# centos软件源配置

备份配置文件: 
```
cp -a /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
```
修改CentOS-Base.repo文件
```
sed -i "s/#baseurl/baseurl/g" /etc/yum.repos.d/CentOS-Base.repo
sed -i "s/mirrorlist=http/#mirrorlist=http/g" /etc/yum.repos.d/CentOS-Base.repo
sed -i "s@http://mirror.centos.org@https://repo.huaweicloud.com@g" /etc/yum.repos.d/CentOS-Base.repo
```
执行yum clean all清除原有yum缓存。

执行yum makecache(刷新缓存)或者yum repolist all(查看所有配置可以使用的文件, 会自动刷新缓存)。
