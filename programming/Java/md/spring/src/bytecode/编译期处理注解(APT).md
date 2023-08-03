# 编译期处理注解(APT)

按照处理时期，注解分为两种类型，一种是运行时注解，另一种是编译时注解

编译时注解的核心依赖APT(Annotation Processing Tools)实现，对应的处理流程为：

- 在某些代码元素上（如类型、函数、字段等）添加注解
- 编译时编译器会检查AbstractProcessor的子类
- 然后将添加了注解的所有元素都传递到该类的process函数中，使得开发人员可以在编译器进行相应的处理，比如动态生成代码

# POM

注意：不能将AbstractProcessor和使用该AbstractProcessor的类写在同一个项目中，会因为AbstractProcessor没有预编译导致报错。

父模块

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>org.example</groupId>
  <artifactId>untitled3</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <name>untitled3</name>
  <modules>
    <module>m1</module>
    <module>m2</module>
  </modules>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>8</maven.compiler.source>
    <maven.compiler.target>8</maven.compiler.target>
  </properties>

  <dependencies>
  </dependencies>
</project>
```

子模块1：定义编译时注解处理器

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.example</groupId>
    <artifactId>untitled3</artifactId>
    <version>1.0-SNAPSHOT</version>
  </parent>

  <artifactId>m1</artifactId>
  <packaging>jar</packaging>

  <name>m1</name>
  <!-- 没有这个配置编译时会报错:提示服务配置文件不正确, 或构造处理程序对象 Processor not found -->
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration>
          <!-- 避免编译时使用自身的DemoProcessor，因为自定义的DemoProcessor还没被编译生成 -->
          <compilerArgument>-proc:none</compilerArgument>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

子模块2：使用编译时注解

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.example</groupId>
    <artifactId>untitled3</artifactId>
    <version>1.0-SNAPSHOT</version>
  </parent>

  <artifactId>m2</artifactId>
  <packaging>jar</packaging>

  <name>m2</name>

  <dependencies>
    <dependency>
      <groupId>org.example</groupId>
      <artifactId>m1</artifactId>
      <version>1.0-SNAPSHOT</version>
    </dependency>
  </dependencies>
</project>
```

# 创建一个注解

```java
package org.m1;

public @interface M1A {
}
```

# 创建对应的注解处理器

```java
package org.m1;

import com.google.auto.service.AutoService;

import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.TypeElement;
import javax.tools.JavaFileObject;
import java.io.IOException;
import java.io.Writer;
import java.util.Set;

// 指定可以处理的注解
@SupportedAnnotationTypes({"org.m1.M1A"})
// jdk版本
@SupportedSourceVersion(SourceVersion.RELEASE_8)
public class DemoProcessor extends AbstractProcessor {

    public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
        // 创建动态代码
        StringBuilder builder = new StringBuilder()
                .append("package org.ex.m1;\n\n")
                .append("public class GeneratedClass {\n\n")
                .append("\tpublic String getMessage() {\n")
                .append("\t\treturn \"");

        // 获取所有被M1A修饰的代码元素
        for (Element element : roundEnv.getElementsAnnotatedWith(M1A.class)) {
            String objectType = element.getSimpleName().toString();
            builder.append(objectType).append(" exists!\\n");
        }

        builder.append("\";\n")
                .append("\t}\n")
                .append("}\n");

        // 将String写入并生成.class文件
        try {
            JavaFileObject source = processingEnv.getFiler().createSourceFile("org.ex.m1.GeneratedClass");
            Writer writer = source.openWriter();
            writer.write(builder.toString());
            writer.flush();
            writer.close();
            // 注解处理器的日志都要使用Messager发送，最终会以编译结果的形式呈现出来
            this.processingEnv.getMessager().printMessage(Diagnostic.Kind.NOTE, "生成成功");
        } catch (IOException e) {
            this.processingEnv.getMessager().printMessage(Diagnostic.Kind.ERROR, e.toString());
        }
        return true;
    }
}
```

# 使用注解

```java
package org.m2;

import org.m1.M1A;

public class Test {

    @M1A
    public void t() {

    }
}
```

# 使用动态生成的类

```java
package org.m2;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class App {
    public static void main(String[] args) throws Exception {
        Class<?> aClass = Class.forName("org.ex.m1.GeneratedClass");
        Method getMessage = aClass.getMethod("getMessage");
        Constructor<?> constructor = aClass.getConstructor();
        Object o = constructor.newInstance();
        System.out.println(getMessage.invoke(o));
    }
}
```

# 增加配置文件

1. 在m1模块的main目录下，创建resources目录
2. 在resources目录下创建META-INF目录
3. 在META-INF目录下创建services目录
4. 在services目录下创建名为javax.annotation.processing.Processor的文件

在文件内容中指定注解处理器：

```
org.m1.DemoProcessor
```

# 编译

IDE会缓存上一次生成的类文件，所以需要每次都mvn clean

mvn clean -> mvn install -> 运行main

在target目录下就会自动生成一个org.ex.m1.GeneratedClass类

# 使用@AutoService自动生成javax.annotation.processing.Processor文件

## 添加依赖

```xml
<dependency>
  <groupId>com.google.auto.service</groupId>
  <artifactId>auto-service</artifactId>
  <version>1.0-rc7</version>
</dependency>
```

## 修改DemoProcessor

```java
// 用来自动注册APT文件
@AutoService(Processor.class)
@SupportedAnnotationTypes({"org.m1.M1A"})
@SupportedSourceVersion(SourceVersion.RELEASE_8)
public class DemoProcessor extends AbstractProcessor {
  //
}
```

使用AutoService后，自己的javax.annotation.processing.Processor文件可以删除了，m1模块的pom中maven-jar-plugin插件也可以删除了
