# 下载Excel模板文件损坏

maven插件打包项目的时候，默认会压缩resources目录下的文件，excel文件被压缩后就会损坏

# pom.xml配置文件过滤

```xml
<build>
    <resources>
        <!-- 后缀是.xlsx的文件不是资源文件，其它的资源文件需要被过滤 -->
        <resource>
            <directory>src/main/resources</directory>
            <excludes>
                <exclude>**/*.xlsx</exclude>
            </excludes>
            <filtering>true</filtering>
        </resource>
        <!-- 后缀是.xlsx的文件是资源文件，但是不会被过滤 -->
        <resource>
            <directory>src/main/resources</directory>
            <includes>
                <include>**/*.xlsx</include>
            </includes>
            <filtering>false</filtering>
        </resource>
    </resources>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-resources-plugin</artifactId>
            <version>3.0.2</version>
            <configuration>
                <encoding>UTF-8</encoding>
                <nonFilteredFileExtensions>
                    <nonFilteredFileExtension>xlsx</nonFilteredFileExtension>
                    <nonFilteredFileExtension>xls</nonFilteredFileExtension>
                </nonFilteredFileExtensions>
            </configuration>
        </plugin>
    </plugins>
</build>
```
