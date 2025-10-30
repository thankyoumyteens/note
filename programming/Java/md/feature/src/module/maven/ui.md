# ui 模块

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

    <artifactId>ui</artifactId>
    <packaging>jar</packaging>

    <name>ui</name>

    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>calculator-impl</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <configuration>
                    <!-- 声明主类 -->
                    <archive>
                        <manifest>
                            <mainClass>com.example.App</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### 2. module-info.java

```java
import com.example.api.Calculate;

module calculator.ui {
    requires calculator.api;

    uses Calculate;
}
```

### 3. App.java

```java
package com.example;

import com.example.api.Calculate;

import java.util.ServiceLoader;

public class App {
    public static void main(String[] args) {
        Calculate calculator = null;
        ServiceLoader<Calculate> implList = ServiceLoader.load(Calculate.class);
        for (Calculate impl : implList) {
            System.out.println("使用" + impl.getClass().getSimpleName());
            calculator = impl;
            break;
        }
        if (calculator != null) {
            System.out.println(calculator.add(1, 2));
        }
    }
}
```
