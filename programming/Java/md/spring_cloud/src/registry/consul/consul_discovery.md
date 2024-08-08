# 服务发现

1. 修改服务提供方的启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
public class ConsulClientDemo {
    public static void main(String[] args) {
        SpringApplication.run(ConsulClientDemo.class, args);
    }
}
```

2. 查询注册中心里的所有服务提供方

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/service")
public class ServiceInfoController {

    @Autowired
    private DiscoveryClient discoveryClient;

    /**
     * 查询注册中心里的所有服务提供方
     */
    @RequestMapping("/list")
    public List<String> serviceList() {
        // 获取服务的 service ID
        List<String> allServices = discoveryClient.getServices();
        return allServices;
    }
}
```

3. 接口返回

```json
["consul", "consul-client-demo"]
```
