# 过滤器

定义一个简单的 Zuul 过滤器, 它实现了在请求被路由之前检查 HttpServletRequest 中是否有 Authorization, 若有就进行路由, 若没有就拒绝访问, 返回 401 Unauthorized 错误。

1. 添加过滤器

```java
import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.context.RequestContext;
import com.netflix.zuul.exception.ZuulException;

import javax.servlet.http.HttpServletRequest;

public class AccessFilter extends ZuulFilter {
    @Override
    public String filterType() {
        // 路由之前拦截
        return "pre";
    }

    @Override
    public int filterOrder() {
        // 过滤器的执行顺序
        return 0;
    }

    @Override
    public boolean shouldFilter() {
        // 指定过滤器的有效范围, 这里是对所有请求都会生效
        return true;
    }

    @Override
    public Object run() throws ZuulException {
        RequestContext currentContext = RequestContext.getCurrentContext();
        HttpServletRequest request = currentContext.getRequest();

        String authorization = request.getHeader("Authorization");
        if (authorization == null || authorization.isEmpty()) {
            // 不对请求进行路由
            currentContext.setSendZuulResponse(false);
            // 设置响应状态码
            currentContext.setResponseStatusCode(401);
            // 设置响应内容
            currentContext.setResponseBody("Authorization is empty");
            return null;
        }
        // 放行
        return null;
    }
}
```

2. 注入过滤器

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FilterConfig {

    @Bean
    public AccessFilter accessFilter() {
        return new AccessFilter();
    }
}
```

3. 服务启动后, 访问 http://localhost:27440/service1/service/list, 请求头不加 Authorization 的话, 会返回 Authorization is empty
