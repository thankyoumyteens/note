# 查看maven引入jar包的传递依赖

在pom.xml文件的目录下使用
```
mvn dependency:tree -Dverbose -Dincludes=<groupId>:<artifactId>
```
命令可以查看jar包的传递依赖。

- `-Dverbose` 列出更详细的信息
- `-Dincludes=<groupId>:<artifactId>` 输出仅包含这个Jar包的依赖树
