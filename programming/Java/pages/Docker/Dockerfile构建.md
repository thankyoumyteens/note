# docker build

docker build命令用于从Dockerfile构建镜像。

```
docker build  -t ImageName:TagName dir
```

- `-t` 给镜像加一个Tag
- `-f` 指定要使用的Dockerfile路径, 如果不指定, 则在当前工作目录寻找Dockerfile文件
- ImageName 给镜像起的名称
- TagName 给镜像的Tag名
- dir Dockerfile所在目录

# 例子

```
[root@qikegu myImg]# docker build -t myimg:0.1 .
```
- `.` 表示当前目录, 即Dockerfile所在目录

