# 启动多个服务提供方

application.yml 中不指定 `server.port` 属性。IDEA 的 `Run/Debug Configurations` 中复制几个项目启动配置, 在 JVM 参数中使用 `-Dserver.port=端口号` 指定不同的端口。
