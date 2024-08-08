# 如何保证消息不丢失

正常的消息发送过程:

```
生产者 -> 交换机 -> 队列 -> 消费者
```

消息丢失的情况:

1. 生产者发送到交换机失败
2. mq 宕机
3. 消费者消费失败

## 生产者确认机制 (publish confirm)

开启之后, 消息发送到 mq 以后, 会返回一个结果给生产者

- 如果发送到交换机失败, 会返回 publish-confirm 的 nack
- 如果交换机发送到队列失败, 会返回 publish-return 的 ack

失败后的处理方案:

- 失败后重发
- 记录日志
- 保存到数据库, 定时重发

## 消息持久化

mq 默认使用内存保存消息, 开启持久化可以保证 mq 宕机后消息不丢失。

需要设置三个持久化:

1. 交换机持久化, 在声明时指定 durable 为 true
   ```java
   // 三个参数分别为 交换器名、交换器类型、是否持久化
   channel.exchangeDeclare(EXCHANGE_NAME, "topic", true);
   ```
2. 队列持久化, 在声明时指定 durable 为 true
   ```java
   // 参数1 queue : 队列名
   // 参数2 durable : 是否持久化
   // 参数3 exclusive : 仅创建者可以使用的私有队列, 断开后自动删除
   // 参数4 autoDelete : 当所有消费客户端连接断开后, 是否自动删除队列
   // 参数5 arguments
   channel.queueDeclare(QUEUE_NAME, true, false, false, null);
   ```
3. 消息持久化, 在投递时指定 delivery_mode=2
   ```java
   // 参数1 exchange : 交换器
   // 参数2 routingKey :  路由键
   // 参数3 props :  消息的其他参数,其中 MessageProperties.PERSISTENT_TEXT_PLAIN 表示持久化
   // 参数4 body :  消息体
   channel.basicPublish(EXCHANGE_NAME, QUEUE_NAME, MessageProperties.PERSISTENT_TEXT_PLAIN, message.getBytes());
   ```

## 消费者确认

消费者消费后项 mq 发送 ack, mq 收到 ack 后才会删除该消息。如果消费者一直消费失败, 超过重试次数, 会发送一个异常消息给交换机, 手动处理。
