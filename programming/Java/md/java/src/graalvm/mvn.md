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
  <version>1.0</version>
  <packaging>jar</packaging>

  <name>demo</name>

  <properties>
    <!-- 主类的路径 -->
    <mainClass>com.example.MariadbDemo</mainClass>
    <!-- graalvm插件版本 -->
    <native.maven.plugin.version>0.10.3</native.maven.plugin.version>
    <!-- Java版本 -->
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <!-- 要生成的可执行程序名 -->
    <imageName>demo</imageName>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.mariadb.jdbc</groupId>
      <artifactId>mariadb-java-client</artifactId>
      <version>3.5.0</version>
    </dependency>
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>2.0.16</version>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-core</artifactId>
      <version>1.5.7</version>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.5.7</version>
    </dependency>
  </dependencies>

  <profiles>
    <profile>
      <id>native</id>
      <build>
        <plugins>
          <plugin>
            <groupId>org.graalvm.buildtools</groupId>
            <artifactId>native-maven-plugin</artifactId>
            <version>${native.maven.plugin.version}</version>
            <executions>
              <execution>
                <id>build-native</id>
                <goals>
                  <goal>compile-no-fork</goal>
                </goals>
                <phase>package</phase>
              </execution>
              <execution>
                <id>test-native</id>
                <goals>
                  <goal>test</goal>
                </goals>
                <phase>test</phase>
              </execution>
            </executions>
            <configuration>
              <fallback>false</fallback>
            </configuration>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>

  <build>
    <plugins>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.1.1</version>
        <executions>
          <execution>
            <id>java</id>
            <goals>
              <goal>java</goal>
            </goals>
            <configuration>
              <mainClass>${mainClass}</mainClass>
            </configuration>
          </execution>
        </executions>
      </plugin>

      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
        <configuration>
          <source>${maven.compiler.source}</source>
          <target>${maven.compiler.source}</target>
        </configuration>
      </plugin>

      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <archive>
            <manifest>
              <addClasspath>true</addClasspath>
              <mainClass>${mainClass}</mainClass>
            </manifest>
          </archive>
        </configuration>
      </plugin>

      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.6.0</version>
        <executions>
          <execution>
            <phase>package</phase>
            <goals>
              <goal>single</goal>
            </goals>
          </execution>
        </executions>
        <configuration>
          <archive>
            <manifest>
              <addClasspath>true</addClasspath>
              <mainClass>${mainClass}</mainClass>
            </manifest>
          </archive>
          <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
          </descriptorRefs>
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

public class MariadbDemo {
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

mvn -Pnative package
```

### 4. 运行

```sh
./target/demo
```
