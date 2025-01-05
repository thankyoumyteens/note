# 全局异常处理

```java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.web.reactive.error.ErrorWebExceptionHandler;
import org.springframework.core.annotation.Order;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

@Order(-1)
@Component
public class GlobalExceptionHandler implements ErrorWebExceptionHandler {
    @Override
    public Mono<Void> handle(ServerWebExchange serverWebExchange, Throwable throwable) {
        Map<String, Object> result = new HashMap<>();
        ObjectMapper objectMapper = new ObjectMapper();
        ServerHttpResponse response = serverWebExchange.getResponse();
        System.out.println("进入全局异常处理器, 异常信息：" + throwable.getMessage());

        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);

        if (throwable instanceof IllegalArgumentException) {
            result.put("code", 400);
            result.put("message", "参数异常");
        } else {
            result.put("code", 500);
            result.put("message", "服务器异常");
        }
        try {
            return response.writeWith(Mono.just(response.bufferFactory()
                    .wrap(objectMapper.writeValueAsBytes(result))));
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
```
