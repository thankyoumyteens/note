# CentOS 7 安装docker ce
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
使用国内源: 阿里云
```
sudo yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
使用国内源: 腾讯云
```
sudo yum-config-manager \
    --add-repo \
    http://mirrors.cloud.tencent.com/docker-ce/linux/centos/docker-ce.repo
```
更新软件源的缓存, 并安装 Docker
```
sudo yum update
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

# 离线安装

docker安装包下载：https://download.docker.com/linux/centos/7/x86_64/stable/Packages/docker-ce-18.09.8-3.el7.x86_64.rpm

依赖包下载：

containerd.io：https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.2-3.el7.x86_64.rpm

docker-ce-cli：https://download.docker.com/linux/centos/7/x86_64/stable/Packages/docker-ce-cli-18.09.8-3.el7.x86_64.rpm

container-selinux：https://pkgs.org/download/container-selinux

安装
```
rpm -ivh docker-ce-cli-18.09.8-3.el7.x86_64.rpm
rpm -ivh container-selinux-2.107-3.el7.noarch.rpm
rpm -ivh containerd.io-1.2.2-3.el7.x86_64.rpm
rpm -ivh docker-ce-18.09.8-3.el7.x86_64.rpm
```
启动
```
systemctl start docker 
```
查看状态
```
systemctl status docker 
```
