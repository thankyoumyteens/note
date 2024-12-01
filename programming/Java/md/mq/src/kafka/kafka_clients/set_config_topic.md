# 修改 topic 配置

```java
Map<ConfigResource, Collection<AlterConfigOp>> configMap = new HashMap<>();
ConfigResource cfg = new ConfigResource(ConfigResource.Type.TOPIC, "topic2");
ConfigEntry configEntry = new ConfigEntry("cleanup.policy", "compact");
AlterConfigOp op = new AlterConfigOp(configEntry, AlterConfigOp.OpType.SET);
configMap.put(cfg, List.of(op));
adminClient.incrementalAlterConfigs(configMap);
```
