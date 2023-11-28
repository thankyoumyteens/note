# 下载

[https://github.com/fatedier/frp/releases](https://github.com/fatedier/frp/releases)

# 部署

解压缩下载的压缩包, 将其中的 frpc 拷贝到内网服务所在的机器上, 将 frps 拷贝到具有公网 IP 的机器上, 放置在任意目录

# 使用

启动服务端

```
./frps -c ./frps.ini
```

启动客户端

```
./frpc -c ./frpc.ini
```
