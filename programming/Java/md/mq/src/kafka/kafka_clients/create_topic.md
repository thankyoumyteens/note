# 创建 topic

```java
List<NewTopic> topics = List.of(
        // 参数: topic名称，分区数，副本数
        new NewTopic("topic1", 1, (short) 1),
        new NewTopic("topic2", 1, (short) 1)
);
adminClient.createTopics(topics);
```
