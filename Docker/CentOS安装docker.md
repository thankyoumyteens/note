# CentOS 7.6 安装docker ce

## 卸载旧版本

旧版本的 Docker 被叫做 docker 或 docker-engine, 如果您安装了旧版本的 Docker , 您需要卸载掉它。
```
$ sudo yum remove docker \
      docker-client \
      docker-client-latest \
      docker-common \
      docker-latest \
      docker-latest-logrotate \
      docker-logrotate \
      docker-engine
```

## 安装

为了方便添加软件源, 支持 devicemapper 存储类型, 安装如下软件包
```
$ sudo yum update
$ sudo yum install -y yum-utils \
    device-mapper-persistent-data \
    lvm2
```
添加 Docker 稳定版本的 yum 软件源
```
$ sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```
更新一下 yum 软件源的缓存, 并安装 Docker
```
$ sudo yum update
$ sudo yum install docker-ce
```
如果弹出 GPG key 的接收提示, 请确认是否为 060a 61c5 1b55 8a7f 742b 77aa c52f eb6b 621e 9f35, 如果是, 可以接受并继续安装。

至此, Docker 已经安装完成了, Docker 服务是没有启动的, 操作系统里的 docker 组被创建, 但是没有用户在这个组里。

默认的 docker 组是没有用户的（也就是说需要使用 sudo 才能使用 docker 命令）。
您可以将用户添加到 docker 组中（此用户就可以直接使用 docker 命令了）。

加入 docker 用户组命令
```
$ sudo usermod -aG docker USER_NAME
```
用户更新组信息后, 重新登录系统即可生效。

启动 docker 服务
```
$ sudo systemctl start docker
```
验证 Docker CE 安装是否正确, 可以运行 hello-world 镜像
```
$ sudo docker run hello-world
```
