# 延迟队列

延迟队列由死信队列+TTL 组成。TTL 是消息的生存时间。

使用场景:

- 超时取消订单
- 限时优惠
- 定时发布

## 延迟队列插件

RabbitMQ 有一个 rabbitmq_delayed_message_exchange 插件, 也可以实现延迟队列。

安装后, 在声明交换机时只需要把 delayed 属性设置为 true。在发消息时就可以通过 x-delay 设置延迟时间。
