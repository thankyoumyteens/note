# 使用 WebSocket

1. 添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

2. 配置类

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

3. 服务器

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import javax.websocket.*;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Component
// 连接地址 ws://ip:端口/wsDemo/用户Id
@ServerEndpoint("/wsDemo/{userId}")
public class WsDemoServer {

    private static final ConcurrentHashMap<String, WsDemoServer> CLIENTS = new ConcurrentHashMap<>();

    private Session session;

    private String userId;

    @OnOpen
    public void onOpen(Session session, @PathParam("userId") String userId) {
        this.session = session;
        this.userId = userId;
        if (CLIENTS.containsKey(userId)) {
            CLIENTS.remove(userId);
            CLIENTS.put(userId, this);
        } else {
            CLIENTS.put(userId, this);
        }
        log.info("新连接: {}", userId);
        try {
            sendMessage("连接成功");
        } catch (IOException e) {
            log.error("用户{}连接失败", userId, e);
        }
    }

    @OnClose
    public void onClose() {
        CLIENTS.remove(userId);
        log.info("用户{}断开连接", userId);
    }

    @OnMessage
    public void onMessage(String message, Session session) {
        log.info("用户消息:" + userId + ",报文:" + message);
        try {
            JSONObject jsonObject = JSON.parseObject(message);
            jsonObject.put("fromUserId", this.userId);
            String toUserId = jsonObject.getString("toUserId");
            if (CLIENTS.containsKey(toUserId)) {
                CLIENTS.get(toUserId).sendMessage(jsonObject.toJSONString());
            } else {
                log.error("userId:{}不存在", toUserId);
            }
        } catch (Exception e) {
            log.error("{}发送消息失败", userId, e);
        }
    }

    @OnError
    public void onError(Session session, Throwable error) {
        log.error("异常:{},原因:{}", this.userId, error.getMessage());
    }

    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }

}
```
