# 安装 nacos

```sh
wget https://github.com/alibaba/nacos/releases/download/2.4.3/nacos-server-2.4.3.tar.gz
tar -zxvf nacos-server-2.4.3.tar.gz
cd nacos/bin/

# 云服务器需要开放8848, 9848 和 9849 端口
sh startup.sh -m standalone
```
