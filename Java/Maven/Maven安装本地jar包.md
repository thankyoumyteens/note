# 把第三方 jar 包导入本地仓库
方法1
```shell
mvn install:install-file -DgroupId="com.example" -DartifactId="common_util" -Dversion="1.1.3-SNAPSHOT" -Dfile="common_util-1.1.3-SNAPSHOT.jar" -Dpackaging="jar"
```

- DgroupId=com.extend　:　　group名称
- DartifactId=ss_css2　:　　打包后的名称
- Dversion=1.0.0　　　　:　　打包后的版本
- Dpackaging=jar　　　　:　　打包成什么类型

方法2
```xml
<dependency>
    <groupId>css2parser</groupId>
    <artifactId>ss_css2</artifactId>
    <scope>system</scope>
    <systemPath>${basedir}/src/main/resources/libs/ss_css2.jar</systemPath>
</dependency>
```
注解:${basedir}是项目的根目录
