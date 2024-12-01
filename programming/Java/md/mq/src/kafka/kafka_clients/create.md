# 连接 kafka

```java
Properties properties = new Properties();
// kafka服务器地址
properties.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
AdminClient adminClient = AdminClient.create(properties);

adminClient.close();
```
