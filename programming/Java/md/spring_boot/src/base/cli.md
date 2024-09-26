# 命令行项目

1. 实现 CommandLineRunner 接口

```java
package com.example.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class ConsoleApp implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("Hello, world!");
    }
}
```
