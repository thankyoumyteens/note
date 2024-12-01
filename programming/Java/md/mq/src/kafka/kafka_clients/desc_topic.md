# 获取 topic 详情

```java
DescribeTopicsResult desc = adminClient.describeTopics(List.of("topic2"));
KafkaFuture<Map<String, TopicDescription>> descMap = desc.allTopicNames();
Map<String, TopicDescription> map = descMap.get();
for (Map.Entry<String, TopicDescription> entry : map.entrySet()) {
    System.out.println("topic: " + entry.getKey());
    System.out.println("desc: " + entry.getValue());
}
```
