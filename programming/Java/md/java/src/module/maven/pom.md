# 父 pom

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
    http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>jpms-maven-demo</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <name>jpms-maven-demo</name>
    <modules>
        <module>ui</module>
        <module>calculator</module>
        <module>calculator-impl</module>
    </modules>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>

    </dependencies>

    <!-- 统一插件版本 -->
    <build>
        <pluginManagement>
            <plugins>
                <!-- 编译插件：支持 JPMS 模块化编译 -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.12.1</version>
                    <configuration>
                        <source>21</source>
                        <target>21</target>
                        <release>21</release>
                        <!-- Maven 会自动识别 module-info.java -->
                    </configuration>
                </plugin>

                <!-- JAR 打包插件：生成模块化 JAR -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-jar-plugin</artifactId>
                    <version>3.3.0</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```
