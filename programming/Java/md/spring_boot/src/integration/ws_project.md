# 使用 WebSocket

### 1. 添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

### 2. 配置类

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.server.standard.ServerEndpointExporter;

@Configuration
@EnableWebSocket
public class WebSocketConfiguration {

    @Bean
    public ServerEndpointExporter serverEndpointExporter() {
        return new ServerEndpointExporter();
    }

}
```

### 3. 服务器

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import demo.model.dto.MyDTO;
import demo.service.MyService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.websocket.*;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Component
@ServerEndpoint("/myWs") // 连接地址 -> ws://IP:端口/myWs
public class MyWebSocketServer {

    @Resource
    private MyService myService;

    // 解决Component 注入Service 为 null
    // 通过serviceHandler使用service
    private static MyWebSocketServer serviceHandler;

    @PostConstruct
    public void init() {
        serviceHandler = this;
        serviceHandler.myService = this.myService;
    }

    private static final ConcurrentHashMap<String, MyWebSocketServer> CLIENTS = new ConcurrentHashMap<>();

    private Session session;

    private String userId;

    @OnOpen
    public void onOpen(Session session) {
        String userId = UUID.randomUUID().toString();
        this.session = session;
        this.userId = userId;
        if (CLIENTS.containsKey(userId)) {
            CLIENTS.remove(userId);
            CLIENTS.put(userId, this);
        } else {
            CLIENTS.put(userId, this);
        }
        log.info("新连接 userId: {}", userId);
        try {
            sendMessage("连接成功");
        } catch (IOException e) {
            log.error("用户 {} 连接失败", userId, e);
        }
    }

    @OnClose
    public void onClose() {
        CLIENTS.remove(userId);
        serviceHandler.myService.clearCache(userId);
        log.info("用户 {} 断开连接", userId);
    }

    @OnMessage
    public void onMessage(String message, Session session) {
        log.info("用户: {}, 消息: {}", userId, message);
        try {
            MyDTO p = JSON.parseObject(message, MyDTO.class);
            serviceHandler.myService.doSth(userId, session, p);
        } catch (Exception e) {
            log.error("用户 {} 发送消息失败", userId, e);
        }
    }

    @OnError
    public void onError(Session session, Throwable error) {
        log.error("用户: {} , 异常: {}", this.userId, error.getMessage());
    }

    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }

}
```
