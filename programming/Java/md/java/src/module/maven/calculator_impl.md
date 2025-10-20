# calculator-impl 模块

### 1. pom 文件

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
    http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.example</groupId>
        <artifactId>jpms-maven-demo</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>calculator-impl</artifactId>
    <packaging>jar</packaging>

    <name>calculator-impl</name>

    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>calculator</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- 继承父 POM 的编译和打包插件，无需额外配置 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### 2. module-info.java

```java
import com.example.api.Calculate;
import com.example.impl.SimpleCalculator;

module calculator.impl {
    requires calculator.api;

    provides Calculate with SimpleCalculator;
}
```

### 3. SimpleCalculator.java

```java
package com.example.impl;

import com.example.api.Calculate;

public class SimpleCalculator implements Calculate {
    @Override
    public int add(int a, int b) {
        return a + b;
    }
}
```
