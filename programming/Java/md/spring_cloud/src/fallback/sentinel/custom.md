# 自定义限流时返回的信息

指定 `@SentinelResource` 的 `blockHandler` 属性:

```java
import com.alibaba.csp.sentinel.annotation.SentinelResource;
import com.alibaba.csp.sentinel.slots.block.BlockException;
import org.springframework.stereotype.Service;

@Service
public class DemoService {

    @SentinelResource(value = "demo", blockHandler = "exceptionHandler")
    public String demo() {
        return "hello";
    }

    public String exceptionHandler(String p1, String p2, BlockException ex) {
        return "自定义返回的异常信息";
    }
}
```
