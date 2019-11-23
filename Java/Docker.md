# Docker安装与启动

## 安装Docker 

（1）yum 包更新到最新
```
sudo yum update
```
（2）安装需要的软件包， yum-util 提供yum-config-manager功能，另外两个是devicemapper驱动依赖的
```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```
（3）设置yum源为阿里云
```
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
（4）安装docker
```
sudo yum install docker-ce
```
（5）安装后查看docker版本
```
docker -v
```

## 设置ustc的镜像 

ustc是老牌的linux镜像服务提供者了，还在遥远的ubuntu 5.04版本的时候就在用。ustc的docker镜像加速器速度很快。ustc docker mirror的优势之一就是不需要注册，是真正的公共服务。

编辑该文件：

```
vi /etc/docker/daemon.json  
```

在该文件中输入如下内容：

```
{
"registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
```

## Docker的启动与停止

启动docker：
```
systemctl start docker
```
停止docker：
```
systemctl stop docker
```
重启docker：
```
systemctl restart docker
```
查看docker状态：
```
systemctl status docker
```
开机启动：
```
systemctl enable docker
```
查看docker概要信息
```
docker info
```
查看docker帮助文档
```
docker --help
```

# 镜像相关命令

## 查看镜像

```
docker images
```

* REPOSITORY：镜像名称
* TAG：镜像标签
* IMAGE ID：镜像ID
* CREATED：镜像的创建日期（不是获取该镜像的日期）
* SIZE：镜像大小

这些镜像都是存储在Docker宿主机的`/var/lib/docker`目录下

## 搜索镜像

如果你需要从网络中查找需要的镜像，可以通过以下命令搜索

```
docker search 镜像名称
```

* NAME：仓库名称
* DESCRIPTION：镜像描述
* STARS：用户评价，反应一个镜像的受欢迎程度
* OFFICIAL：是否官方
* AUTOMATED：自动构建，表示该镜像由Docker Hub自动构建流程创建的

## 拉取镜像

拉取镜像就是从中央仓库中下载镜像到本地

```
docker pull 镜像名称
```
例如，下载centos7镜像
```
docker pull centos:7
```

## 删除镜像

按镜像ID删除镜像
```
docker rmi 镜像ID
```
删除所有镜像
```
docker rmi `docker images -q`
```

# 容器相关命令

## 查看容器

查看正在运行的容器
```
docker ps
```
查看所有容器
```
docker ps –a
```
查看最后一次运行的容器
```
docker ps –l
```
查看停止的容器
```
docker ps -f status=exited
```

## 创建与启动容器

创建容器常用的参数说明：

创建容器命令：`docker run`

* -i：表示运行容器
* -t：表示容器启动后会进入其命令行。加入这两个参数后，容器创建就能登录进去。即分配一个伪终端。
* --name :为创建的容器命名。
* -v：表示目录映射关系（前者是宿主机目录，后者是映射到宿主机上的目录），可以使用多个－v做多个目录或文件映射。注意：最好做目录映射，在宿主机上做修改，然后共享到容器上。
* -d：在run后面加上-d参数,则会创建一个守护式容器在后台运行（这样创建容器后不会自动登录容器，如果只加-i -t两个参数，创建后就会自动进去容器）。
* -p：表示端口映射，前者是宿主机端口，后者是容器内的映射端口。可以使用多个-p做多个端口映射

（1）交互式方式创建容器
```
docker run -it --name=容器名称 镜像名称:标签 /bin/bash
```
这时我们通过ps命令查看，发现可以看到启动的容器，状态为启动状态  

退出当前容器
```
exit
```
（2）守护式方式创建容器：
```
docker run -di --name=容器名称 镜像名称:标签
```
登录守护式容器方式：
```
docker exec -it 容器名称 (或者容器ID)  /bin/bash
```

## 停止与启动容器

停止容器：
```
docker stop 容器名称（或者容器ID）
```
启动容器：

```
docker start 容器名称（或者容器ID）
```

## 文件拷贝

如果我们需要将文件拷贝到容器内可以使用cp命令
```
docker cp 需要拷贝的文件或目录 容器名称:容器目录
```
也可以将文件从容器内拷贝出来
```
docker cp 容器名称:容器目录 需要拷贝的文件或目录
```

## 目录挂载

我们可以在创建容器的时候，将宿主机的目录与容器内的目录进行映射，这样我们就可以通过修改宿主机某个目录的文件从而去影响容器。
创建容器 添加-v参数 后边为   宿主机目录:容器目录，例如：
```
docker run -di -v /usr/local/myhtml:/usr/local/myhtml --name=mycentos3 centos:7
```

如果你共享的是多级的目录，可能会出现权限不足的提示。

这是因为CentOS7中的安全模块selinux把权限禁掉了，我们需要添加参数`--privileged=true`来解决挂载的目录没有权限的问题

## 查看容器IP地址

我们可以通过以下命令查看容器运行的各种数据
```
docker inspect 容器名称（容器ID） 
```
也可以直接执行下面的命令直接输出IP地址
```
docker inspect --format='{{.NetworkSettings.IPAddress}}' 容器名称（容器ID）
```

## 删除容器 

删除指定的容器：
```
docker rm 容器名称（容器ID）
```

# 应用部署

## MySQL部署

（1）拉取mysql镜像
```
docker pull centos/mysql-57-centos7
```
（2）创建容器
```
docker run -di --name=tensquare_mysql -p 33306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

* -p 代表端口映射，格式为  宿主机映射端口:容器运行端口
* -e 代表添加环境变量  MYSQL_ROOT_PASSWORD  是root用户的登陆密码

 ## tomcat部署

（1）拉取镜像
```
docker pull tomcat:7-jre7
```
（2）创建容器
```
docker run -di --name=mytomcat -p 9000:8080 -v /usr/local/webapps:/usr/local/tomcat/webapps tomcat:7-jre7
```

## Nginx部署 

（1）拉取镜像	
```
docker pull nginx
```
（2）创建Nginx容器
```
docker run -di --name=mynginx -p 80:80 nginx
```

## Redis部署

（1）拉取镜像
```
docker pull redis
```
（2）创建容器
```
docker run -di --name=myredis -p 6379:6379 redis
```

# 迁移与备份

## 容器保存为镜像

我们可以通过以下命令将容器保存为镜像
```
docker commit mynginx mynginx_i
```

## 镜像备份

我们可以通过以下命令将镜像保存为tar 文件
```
docker  save -o mynginx.tar mynginx_i
```

## 镜像恢复与迁移

首先我们先删除掉mynginx_img镜像  然后执行此命令进行恢复
```
docker load -i mynginx.tar
```

* -i 输入的文件

执行后再次查看镜像，可以看到镜像已经恢复

# Dockerfile

## 什么是Dockerfile

Dockerfile是由一系列命令和参数构成的脚本，这些命令应用于基础镜像并最终创建一个新的镜像。

1. 对于开发人员：可以为开发团队提供一个完全一致的开发环境； 
2. 对于测试人员：可以直接拿开发时所构建的镜像或者通过Dockerfile文件构建一个新的镜像开始工作了； 
3. 对于运维人员：在部署时，可以实现应用的无缝移植。

## 常用命令

| 命令                                 | 作用                                 |
| ---------------------------------- | ---------------------------------- |
| FROM image_name:tag                | 定义了使用哪个基础镜像启动构建流程                  |
| MAINTAINER user_name               | 声明镜像的创建者                           |
| ENV key value                      | 设置环境变量 (可以写多条)                     |
| RUN command                        | 是Dockerfile的核心部分(可以写多条)            |
| ADD source_dir/file dest_dir/file  | 将宿主机的文件复制到容器内，如果是一个压缩文件，将会在复制后自动解压 |
| COPY source_dir/file dest_dir/file | 和ADD相似，但是如果有压缩文件并不能解压              |
| WORKDIR path_dir                   | 设置工作目录                             |

## 使用脚本创建镜像

步骤：

（1）创建目录

```
mkdir –p /usr/local/dockerjdk8
```

（2）下载jdk-8u171-linux-x64.tar.gz并上传到服务器（虚拟机）中的/usr/local/dockerjdk8目录

（3）创建文件Dockerfile  `vi Dockerfile`

```
#依赖镜像名称和ID
FROM centos:7
#指定镜像创建者信息
MAINTAINER ITCAST
#切换工作目录
WORKDIR /usr
RUN mkdir  /usr/local/java
#ADD 是相对路径jar,把java添加到容器中
ADD jdk-8u171-linux-x64.tar.gz /usr/local/java/

#配置java环境变量
ENV JAVA_HOME /usr/local/java/jdk1.8.0_171
ENV JRE_HOME $JAVA_HOME/jre
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib:$CLASSPATH
ENV PATH $JAVA_HOME/bin:$PATH
```

（4）执行命令构建镜像

```
docker build -t='jdk1.8' .
```

注意后边的空格和点，不要省略

（5）查看镜像是否建立完成

```
docker images
```

# Docker私有仓库

## 私有仓库搭建与配置

（1）拉取私有仓库镜像（此步省略）

```
docker pull registry
```

（2）启动私有仓库容器

```
docker run -di --name=registry -p 5000:5000 registry
```

（3）打开浏览器 输入地址http://192.168.184.141:5000/v2/_catalog看到`{"repositories":[]}` 表示私有仓库搭建成功并且内容为空

（4）修改daemon.json

```
vi /etc/docker/daemon.json
```

添加以下内容，保存退出。

```json
{"insecure-registries":["192.168.184.141:5000"]} 
```

此步用于让 docker信任私有仓库地址

（5）重启docker 服务

```
systemctl restart docker
```

## 镜像上传至私有仓库

（1）标记此镜像为私有仓库的镜像

```
docker tag jdk1.8 192.168.184.141:5000/jdk1.8
```

（2）再次启动私服容器

```
docker start registry
```

（3）上传标记的镜像

```
docker push 192.168.184.141:5000/jdk1.8
```

## 从私有仓库下载镜像

修改daemon.json

```
vi /etc/docker/daemon.json
```

添加以下内容，保存退出。

```json
{"insecure-registries":["192.168.184.141:5000"]} 
```

重启docker 服务

```
systemctl restart docker
```

下载镜像

```
docker pull 192.168.184.141:5000/jdk1.8
```
