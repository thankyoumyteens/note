# FROM
```dockerfile
FROM <image> [AS <name>]
FROM <image>[:<tag>] [AS <name>]
FROM <image>[@<digest>] [AS <name>]
```
指定基础镜像, 当前镜像是基于哪个镜像创建的, 有点类似java中的类继承。FROM指令必是Dockerfile文件中的首条命令。

# LABEL
```dockerfile
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```
给镜像添加元数据。指定一些作者、邮箱等信息。

# ENV
```dockerfile
ENV <key> <value>
ENV <key>=<value> ...
```
设置环境变量, 设置的变量可供后面指令使用。跟java中定义变量差不多的意思

# WORKDIR
```dockerfile
WORKDIR /path/to/workdir
```
设置工作目录, 在该指令后的RUN、CMD、ENTRYPOINT, COPY、ADD指令都会在该目录执行。如果该目录不存在, 则会创建

# RUN
```dockerfile
RUN <command>
RUN ["executable", "param1", "param2"]
```
RUN会在当前镜像的最上面创建一个新层, 并且能执行任何的命令, 然后对执行的结果进行提交。提交后的结果镜像在dockerfile的后续步骤中可以使用。

# ADD
```dockerfile
ADD [--chown=<user>:<group>] <src>... <dest>
ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]
```
从宿主机拷贝文件或者文件夹到镜像, 也可以复制一个网络文件, 如果拷贝的文件是一个压缩包, 会自动解压缩

# COPY
```dockerfile
COPY [--chown=<user>:<group>] <src>... <dest>
COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]
```
从宿主机拷贝文件或者文件夹到镜像, 不能复制网络文件也不会自动解压缩

# VOLUME
```dockerfile
VOLUME ["/data"]
```
创建挂载点, 一般配合run命令的-v参数使用。

# EXPOSE
```dockerfile
EXPOSE <port> [<port>/<protocol>...]
```
指定容器运行时对外暴露的端口, 但是该指定实际上不会发布该端口, 它的功能是镜像构建者和容器运行者之间的记录文件。

run命令的`-P`参数就是随机端口映射, 容器内会随机映射到EXPOSE指定的端口。

# CMD
```dockerfile
CMD ["executable","param1","param2"]
CMD ["param1","param2"]
CMD command param1 param2
```
指定容器启动时默认运行的命令,在一个Dockerfile文件中, 如果有多个CMD命令, 只有一个最后一个会生效

RUN指令是在构建镜像时候执行的, 而CMD指令是在每次容器运行的时候执行的

docker run命令会覆盖CMD的命令

# ENTRYPOINT
```dockerfile
ENTRYPOINT ["executable", "param1", "param2"]
ENTRYPOINT command param1 param2
```
这个指令与CMD指令类似, 都是指定启动容器时要运行的命令, 如果指定了ENTRYPOINT, 则CMD指定的命令不会执行

在一个Dockerfile文件中, 如果有多个ENTRYPOINT命令, 也只有一个最后一个会生效

不同的是通过`docker run command`命令会覆盖CMD的命令, 不会覆盖ENTRYPOINT的命令

docker run命令中指定的任何参数都会被当做参数传递给ENTRYPOINT

## RUN、CMD、ENTRYPOINT区别
1、RUN指令是在镜像构建时运行, 而后两个是在容器启动时执行！
2、CMD指令设置的命令是容器启动时默认运行的命令,如果docker run没有指定任何的命令, 并且Dockerfile中没有指定ENTRYPOINT, 那容器启动的时候就会执行CMD指定的命令！有点类似代码中的缺省参数！
3、如果设置了ENTRYPOINT指令, 则优先使用！并且可以通过docker run给该指令设置的命令传参！
4、CMD有点类似代码中的缺省参数

# USER
```dockerfile
USER <user>[:<group>]
USER <UID>[:<GID>]
```
用于指定运行镜像所使用的用户。

# ARG
```dockerfile
ARG <name>[=<default value>]
```
指定在镜像构建时可传递的变量, 定义的变量可以通过`docker build --build-arg =`的方式在构建时设置。

# ONBUILD
```dockerfile
ONBUILD [INSTRUCTION]
```
当所构建的镜像被当做其他镜像的基础镜像时, ONBUILD指定的命令会被触发！

# STOPSIGNAL
```dockerfile
STOPSIGNAL signal
```
设置当容器停止时所要发送的系统调用信号

# HEALTHCHECK
```dockerfile
HEALTHCHECK [OPTIONS] CMD command (在容器内运行运行命令检测容器的运行情况)
HEALTHCHECK NONE (禁止从父镜像继承检查)
```
该指令可以告诉Docker怎么去检测一个容器的运行状况

# SHELL
```dockerfile
SHELL ["executable", "parameters"]
```
用于设置执行命令所使用的默认的shell类型

该指令在windows操作系统下比较有用, 因为windows下通常会有cmd和powershell两种shell, 甚至还有sh。

