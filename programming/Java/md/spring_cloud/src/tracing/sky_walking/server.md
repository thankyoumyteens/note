# 服务端搭建

1. 下载服务端: [apache-skywalking-apm-10.1.0.tar.gz](https://www.apache.org/dyn/closer.cgi/skywalking/10.1.0/apache-skywalking-apm-10.1.0.tar.gz)
2. 解压

```sh
tar -zxvf apache-skywalking-apm-10.1.0.tar.gz
```

3. 修改 config/application.yml

```yaml
cluster:
  # 改成nacos
  selector: ${SW_CLUSTER:nacos}
  # 配置nacos连接
  nacos:
    serviceName: ${SW_SERVICE_NAME:"SkyWalking_OAP_Cluster"}
    hostPort: ${SW_CLUSTER_NACOS_HOST_PORT:localhost:8848}
    namespace: ${SW_CLUSTER_NACOS_NAMESPACE:"public"}
    contextPath: ${SW_CLUSTER_NACOS_CONTEXT_PATH:""}
    username: ${SW_CLUSTER_NACOS_USERNAME:""}
    password: ${SW_CLUSTER_NACOS_PASSWORD:""}
    accessKey: ${SW_CLUSTER_NACOS_ACCESSKEY:""}
    secretKey: ${SW_CLUSTER_NACOS_SECRETKEY:""}
    internalComHost: ${SW_CLUSTER_INTERNAL_COM_HOST:""}
    internalComPort: ${SW_CLUSTER_INTERNAL_COM_PORT:-1}
```

4. 修改 webapp/application.yml

```yaml
# 指定端口号
serverPort: ${SW_SERVER_PORT:-8080}
```

5. 启动

```sh
cd bin
sh startup.sh
```

6. 访问 http://localhost:9080
