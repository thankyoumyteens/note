# 发布订阅模式

Redis 发布订阅模式是 Redis 提供的一种消息通信机制，允许客户端订阅特定的频道，当有其他客户端向这些频道发布消息时，订阅者会收到相应的消息通知。

- **频道（Channel）**：类似于一个主题或分类，消息发布者将消息发送到特定的频道，而订阅者通过订阅感兴趣的频道来接收相关消息
- **发布者（Publisher）**：负责向指定的频道发送消息的客户端。发布者不需要知道有哪些订阅者正在监听该频道，只需要专注于将消息发布到正确的频道即可
- **订阅者（Subscriber）**：订阅一个或多个频道的客户端，用于接收发布者发送到所订阅频道的消息

## 工作原理

1. **订阅频道**：客户端通过`SUBSCRIBE`命令订阅一个或多个频道。Redis 服务器会维护一个订阅者列表，记录每个频道的订阅者信息
2. **发布消息**：当发布者使用`PUBLISH`命令向某个频道发送消息时，Redis 服务器会遍历该频道的订阅者列表，将消息发送给每个订阅者
3. **接收消息**：订阅者会在自己的连接上接收到来自 Redis 服务器推送的消息，从而实现消息的实时接收

## 示例

### 1. 添加依赖

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>4.4.3</version>
</dependency>
```

### 2. 编写订阅者代码

```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;

// 自定义订阅者类，继承自 JedisPubSub
class MySubscriber extends JedisPubSub {

    // 当成功订阅频道时触发
    @Override
    public void onSubscribe(String channel, int subscribedChannels) {
        System.out.println("Subscribed to channel: " + channel);
    }

    // 当接收到消息时触发
    @Override
    public void onMessage(String channel, String message) {
        System.out.println("Received message from channel " + channel + ": " + message);
    }
}

// 订阅者主类
public class Subscriber {
    public static void main(String[] args) {
        // 创建 Jedis 客户端实例，连接到本地 Redis 服务器
        Jedis jedis = new Jedis("localhost", 6379);
        // 创建自定义订阅者实例
        MySubscriber subscriber = new MySubscriber();
        try {
            // 订阅指定频道
            jedis.subscribe(subscriber, "my_channel");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 关闭 Jedis 连接
            jedis.close();
        }
    }
}
```

### 3. 编写发布者代码

```java
import redis.clients.jedis.Jedis;

// 发布者主类
public class Publisher {
    public static void main(String[] args) {
        // 创建 Jedis 客户端实例，连接到本地 Redis 服务器
        Jedis jedis = new Jedis("localhost", 6379);
        try {
            // 向指定频道发布消息
            jedis.publish("my_channel", "Hello, Redis Pub/Sub!");
            System.out.println("Message published to channel: my_channel");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 关闭 Jedis 连接
            jedis.close();
        }
    }
}
```

### 4. 运行

1. 先运行 `Subscriber` 类，启动订阅者
2. 再运行 `Publisher` 类，启动发布者，发布消息。此时订阅者会接收到发布的消息并输出

## 应用场景

- **实时消息推送**：如实时新闻推送、即时通讯应用中的消息传递等
- **分布式系统中的通知机制**：在分布式系统中，各个节点可以通过 Redis 的发布订阅模式来实现状态通知、任务调度等功能
- **缓存更新通知**：当缓存中的数据发生变化时，可以通过发布订阅模式通知相关的应用程序，使其及时更新缓存或采取相应的措施

## 优缺点

- **优点**：实现简单，能轻松实现一对多的消息通信，适用于实时性要求较高的场景
- **缺点**：不保证消息的可靠性，没有消息确认机制，如果订阅者在消息发布时离线，就会错过消息。同时，它的功能相对简单，对于复杂的消息队列场景，可能无法满足需求
