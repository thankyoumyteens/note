# Web项目

### 1. 修改 `build.gradle` 引入 Web 依赖

打开你的 `build.gradle`，找到 `dependencies` 模块。将原来的基础 `spring-boot-starter` 替换为 `spring-boot-starter-web`。

```groovy
dependencies {
    // 引入 Web 依赖（包含了内嵌 Tomcat、Spring MVC 以及基础 starter 的所有功能）
    implementation 'org.springframework.boot:spring-boot-starter-web'

    // 测试套件
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}
```

_(修改完后，如果你用的是 IDEA，记得点击右上角的 Gradle 刷新图标，让它下载 Tomcat 和 Spring MVC 等相关 Jar 包。)_

---

### 2. 创建 Service 层

我们在项目中创建一个 `service` 包，并编写一个简单的业务逻辑类。

**路径**: `src/main/java/com/example/demo/service/HelloService.java`

```java
package com.example.demo.service;

import org.springframework.stereotype.Service;

@Service
public class HelloService {

    public String generateGreeting(String name) {
        // 使用 Java 现代的字符串模板或简单的拼接
        return "Hello, " + name + "! 欢迎来到 Java 25 与 Spring Boot 4.0.5 的世界。";
    }
}
```

---

### 3. 创建 Controller 层

接着创建一个 `controller` 包，编写对外的 API 接口。这里我们采用**构造器注入**（推荐的最佳实践），并使用 **Java Record** 来作为返回的 JSON 对象。

**路径**: `src/main/java/com/example/demo/controller/HelloController.java`

```java
package com.example.demo.controller;

import com.example.demo.service.HelloService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    private final HelloService helloService;

    // 推荐的构造器注入方式，Spring 会自动装配 HelloService
    public HelloController(HelloService helloService) {
        this.helloService = helloService;
    }

    // 💡 亮点：使用 Java Record 定义响应体，Spring Boot 4 会自动将其转换为 JSON 返回
    public record ApiResponse(int status, String data, String jdkVersion) {}

    @GetMapping("/hello")
    public ApiResponse hello(@RequestParam(defaultValue = "开发者") String name) {
        String message = helloService.generateGreeting(name);
        String version = System.getProperty("java.version");

        // 返回 Record 实例
        return new ApiResponse(200, message, version);
    }
}
```

---

### 4. 运行并测试

确保你的项目现在长这样：

```text
src/main/java/com/example/demo/
 ├── MySpringBootApplication.java  (之前创建的启动类)
 ├── controller/
 │   └── HelloController.java
 └── service/
     └── HelloService.java
```

**启动项目：**

当你在控制台看到类似 `Tomcat started on port 8080 (http) with context path '/'` 的日志后，说明 Web 服务已经启动。

打开浏览器，或者新建一个终端窗口使用 `curl` 访问：

```bash
curl http://localhost:8080/hello
```

你将得到一个漂亮的 JSON 响应：

```json
{
  "status": 200,
  "data": "Hello, 开发者! 欢迎来到 Java 25 与 Spring Boot 4.0.5 的世界。",
  "jdkVersion": "25"
}
```
