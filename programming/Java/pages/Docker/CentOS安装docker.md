# CentOS 7 安装docker ce
卸载旧版本
```
sudo yum remove docker docker-common docker-selinux docker-engine
```
安装软件包
```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```
添加软件源
```
wget -O /etc/yum.repos.d/docker-ce.repo https://repo.huaweicloud.com/docker-ce/linux/centos/docker-ce.repo
```
替换软件仓库地址
```
sudo sed -i 's+download.docker.com+repo.huaweicloud.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
```
更新索引文件并安装 Docker
```
sudo yum makecache fast
sudo yum install docker-ce -y
```
启动 docker 服务
```
sudo systemctl start docker
```
运行 hello-world
```
sudo docker run hello-world
```
设置成开机启动
```
sudo systemctl enable docker
```
