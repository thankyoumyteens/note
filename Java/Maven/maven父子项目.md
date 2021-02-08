# maven子项目父项目

## 项目搭建

项目结构
```
Parent
    childA
    childB
```

在parent的pom文件里加入以下内容。
```xml
<modules>
   <module>childA</module>
   <module>childB</module>
</modules>
```

这样只是告诉maven编译器, 在读取parent的pom文件时去找到childA和childB, 但还是会分别去编译他们引入的依赖。这样就会导致pom文件引入的包重复

于是我们引入了"继承"的概念, 也就是形成"父子"关系, 子pom可以引用到父pom中引入的依赖。

在parent中, 写入以下内容
```xml
<modelVersion>4.0.0</modelVersion>
<groupId>com.module</groupId>
<artifactId>Parent-Module</artifactId>
<version>1.0.2</version>
<packaging>pom</packaging>
<name>Simple-main</name>
```

父pom写好了, 子pom就通过parent标签继承父pom的依赖, 如下：
```xml
<parent>
   <groupId>com.module</groupId>
   <artifactId>Parent-Module</artifactId>
   <version>1.0.2</version>
   <relativePath>../pom.xml</relativePath>
</parent>
```
如果pom的层次关系就像本例中的那样只隔一层, 则可以省略relativePath标签。maven同样可以找到子pom。

子pom中引入parent标签后, 就会从父pom继承version等属性了, 例如childA只需要再加入如下内容即可
```xml
<modelVersion>4.0.0</modelVersion>
<artifactId>ChildA-module</artifactId>
<packaging>jar</packaging>
<name>childA</name>
```

## 添加依赖

解决添加依赖时重复引用jar包, 主pom中把依赖通过dependecyManagement引起来, 表示子pom可能会用到的jar包依赖
```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>servlet-api</artifactId>
      <version>2.5</version>
    </dependency>
   </dependencies>
</dependencyManagement>
```

子pom如果需要引用该jar包, 则直接引用即可, 不需要加入version, 便于统一管理。此外也可以加入仅在子pom中用到的jar包
```xml
<dependencies>
  <!--此处不再需要verison了！-->
  <dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>servlet-api</artifactId>
  </dependency>
  <!--当然也可以加入只在这个子模块中用到的jar包-->
  <dependency>
    <groupId>org.codehaus.jackson</groupId>
    <artifactId>jackson-core-lgpl</artifactId>
    <version>1.9.4</version>    
  </dependency>
</dependencies>
```

## 添加插件

除了jar包依赖, 插件也可以通过这样的方式进行管理

```xml
<!-- parent -->
<build>
  <pluginManagement>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-source-plugin</artifactId>
        <version>2.1.1</version>
      </plugin>
    </plugins>
  </pluginManagement>
</build>

<!-- childA -->
<build>   
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-source-plugin</artifactId>
    </plugin>
  </plugins>
</build>
```

## 子项目互相引用

如果子pom间存在引用关系, 比如childB引用到了childA的jar包
```xml
<dependency>
   <groupId>com.module</groupId>
   <artifactId>childA</artifactId>
   <version>1.0.2</version>
</dependency>
```
