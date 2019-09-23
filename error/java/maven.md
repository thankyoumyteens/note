# maven项目更新后jdk变为1.5

在使用Maven构建项目时，生成的maven项目jdk默认使用的是jdk1.5。
在手动修改了jdk之后，update project之后jdk又会变为1.5.
或者用eclipse的Maven插件生成的也是1.5
对于这种情况有两种办法，一是修改settings.xml，二是修改pom文件

## 1、配置settings.xml
找到 `<profiles>` 节点，并添加如上配置（本机 jdk 1.8.0——25 版本，配置时修改成你本机的 jdk 版本），保存后生效。
```
<profile>    
  <id>jdk-1.8</id>    
  <activation>    
      <activeByDefault>true</activeByDefault>    
      <jdk>1.8</jdk>    
  </activation>    
  <properties>    
      <maven.compiler.source>1.8</maven.compiler.source>    
      <maven.compiler.target>1.8</maven.compiler.target>    
      <maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>    
  </properties>    
</profile>
```

## 2、配置pom.xml文件
配置完成后，需要执行一次更新项目配置的动作。选中项目 --> 右键 --> Maven --> Update Project
```
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <configuration>
        <source>1.8</source>
        <target>1.8</target>
      </configuration>
    </plugin>
  </plugins>
</build>
```
