# 下载

```sh
cd ~/src_pack/
wget https://github.com/docker/compose/releases/download/v2.23.1/docker-compose-linux-x86_64
```

# 重命名

```sh
mv docker-compose-linux-x86_64 docker-compose
```

# 修改权限

```sh
chmod +x docker-compose
```

# 移动文件

```sh
mv docker-compose /usr/local/bin
```

# 配置环境变量

```sh
vim /etc/profile
```

增加: 

```sh
export PATH=$PATH:/usr/local/bin
```

使环境变量生效: 

```sh
source /etc/profile
```

# 查看版本

```sh
docker-compose version
```
