# 把第三方 jar 包导入本地仓库
方法1
```shell
mvn install:install-file -DgroupId="com.example" -DartifactId="common_util" -Dversion="1.1.3-SNAPSHOT" -Dfile="common_util-1.1.3-SNAPSHOT.jar" -Dpackaging="jar" -DgeneratePom=true
```

- `DgroupId=com.extend`: group名称
- `DartifactId=ss_css2`: 打包后的名称
- `Dversion=1.0.0`: 打包后的版本
- `Dpackaging=jar`: 打包成什么类型
- `DgeneratePom`: 是否生成pom文件，ture:生成，false：不生成
- 注意: maven仓库中的jar包, 在同级目录下需要有和jar包同名的`.pom`文件才能正确导入依赖

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
