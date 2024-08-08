# 安装

```sh
wget https://releases.hashicorp.com/consul/1.19.1/consul_1.19.1_linux_amd64.zip
unzip consul_1.19.1_linux_amd64.zip -d ./consul_1.19.1
cd consul_1.19.1/
# 以开发模式启动consul单机服务, 允许外部访问
nohup ./consul agent -dev -client 0.0.0.0 -ui > consul.log &

# 查询所有注册的服务
./consul catalog services
```

访问 http://localhost:8500/ui/ 打开管理页面。
