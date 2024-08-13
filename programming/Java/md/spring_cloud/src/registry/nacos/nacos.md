# Nacos

```sh
wget https://github.com/alibaba/nacos/releases/download/2.4.0.1/nacos-server-2.4.0.1.tar.gz
tar -zxvf nacos-server-2.4.0.1.tar.gz
cd nacos/bin/
# standalone代表着单机模式运行
bash startup.sh -m standalone
```

启动后访问: http://ip:8848/nacos/ 打开管理页面。

另外需要开放 9848 和 9849 端口。
