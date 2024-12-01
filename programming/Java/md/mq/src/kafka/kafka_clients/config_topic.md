# 获取 topic 配置

```java
ConfigResource resource = new ConfigResource(ConfigResource.Type.TOPIC, "topic2");
DescribeConfigsResult configs = adminClient.describeConfigs(List.of(resource));
KafkaFuture<Map<ConfigResource, Config>> configMap = configs.all();
Map<ConfigResource, Config> map = configMap.get();
for (Map.Entry<ConfigResource, Config> entry : map.entrySet()) {
    System.out.println("resource: " + entry.getKey());
    System.out.println("config: " + entry.getValue());
}
```
