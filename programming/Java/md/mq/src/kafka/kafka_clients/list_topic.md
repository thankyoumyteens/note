# 获取 topic 列表

```java
ListTopicsOptions options = new ListTopicsOptions();
// 显示内部topic
options.listInternal(true);
ListTopicsResult topicList = adminClient.listTopics(options);
Set<String> names = topicList.names().get();
for (String name : names) {
    System.out.println(name);
}
```
