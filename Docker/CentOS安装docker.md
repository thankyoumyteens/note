# CentOS 7.6 安装docker ce
卸载旧版本
```
sudo yum remove docker \
      docker-client \
      docker-client-latest \
      docker-common \
      docker-latest \
      docker-latest-logrotate \
      docker-logrotate \
      docker-engine
```
安装软件包
```
sudo yum update
sudo yum install -y yum-utils \
    device-mapper-persistent-data \
    lvm2
```
添加软件源
```
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```
更新软件源的缓存, 并安装 Docker
```
sudo yum update
sudo yum install docker-ce
```
启动 docker 服务
```
sudo systemctl start docker
```
运行 hello-world
```
sudo docker run hello-world
```
