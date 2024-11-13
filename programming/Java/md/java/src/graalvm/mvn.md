# 编译 maven 项目

### 1. 依赖

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
    http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>demo</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>demo</name>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <!-- 主类的路径 -->
    <mainClass>com.example.App</mainClass>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.mariadb.jdbc</groupId>
      <artifactId>mariadb-java-client</artifactId>
      <version>3.5.0</version>
    </dependency>
    <dependency>
      <groupId>com.oracle.database.jdbc</groupId>
      <artifactId>ojdbc6</artifactId>
      <version>11.2.0.4</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
        <configuration>
          <source>21</source>
          <target>21</target>
          <encoding>UTF-8</encoding>
        </configuration>
      </plugin>
      <!-- maven打包插件 -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-shade-plugin</artifactId>
        <version>3.5.2</version>
        <executions>
          <execution>
            <phase>package</phase>
            <goals>
              <goal>shade</goal>
            </goals>
            <configuration>
              <transformers>
                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                  <mainClass>${mainClass}</mainClass>
                </transformer>
              </transformers>
            </configuration>
          </execution>
        </executions>
      </plugin>
      <!-- graalvm打包插件 -->
      <plugin>
        <groupId>org.graalvm.buildtools</groupId>
        <artifactId>native-maven-plugin</artifactId>
        <version>0.10.3</version>
        <executions>
          <execution>
            <id>build-native</id>
            <goals>
              <goal>compile-no-fork</goal>
            </goals>
            <phase>package</phase>
          </execution>
        </executions>
        <configuration>
          <fallback>false</fallback>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

### 2. 启动类

```java
package com.example;

import java.sql.*;

public class App {
    public static void main(String[] args) {
        String url = "jdbc:mariadb://lcalhost:3306/db_test?characterEncoding=UTF-8&useSSL=false";
        String username = "test";
        String password = "123456";

        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String query = "select * from student_info where student_name = ?";
            try (PreparedStatement statement = connection.prepareStatement(query)) {
                statement.setString(1, "tom");
                try (ResultSet resultSet = statement.executeQuery()) {
                    while (resultSet.next()) {
                        String studentId = resultSet.getString("student_id");
                        System.out.println(studentId);
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
```

### 3. 打包

```sh
# 要把JAVA_HOME设置成graalvm
export JAVA_HOME=/Users/walter/walter/jdk/graalvm-jdk-21.0.5+9.1/Contents/Home

mvn package
```

### 4. 运行

```sh
./target/demo
```
