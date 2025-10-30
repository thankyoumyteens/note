# calculator

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

    <artifactId>calculator</artifactId>
    <packaging>jar</packaging>

    <name>calculator</name>

    <dependencies>

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
module calculator.api {
    exports com.example.api;
}
```

### 3. Calculate.java

```java
package com.example.api;

public interface Calculate {

    int add(int a, int b);
}
```
