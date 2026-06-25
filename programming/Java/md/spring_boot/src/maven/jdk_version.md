# 设置项目的 JDK 版本

## 方法 1:配置 settings.xml

```xml
<profiles>
  <profile>
  <id>jdk-25</id>
  <activation>
    <activeByDefault>true</activeByDefault>
    <jdk>25</jdk>
  </activation>
  <properties>
    <maven.compiler.source>25</maven.compiler.source>
    <maven.compiler.target>25</maven.compiler.target>
    <maven.compiler.compilerVersion>25</maven.compiler.compilerVersion>
  </properties>
  </profile>
</profiles>
```

## 方法 2:配置 pom.xml 文件

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.12.1</version>
      <configuration>
        <source>25</source>
        <target>25</target>
      </configuration>
    </plugin>
  </plugins>
</build>
```
