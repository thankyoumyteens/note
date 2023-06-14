# 编译期注解

按照处理时期，注解分为两种类型，一种是运行时注解，另一种是编译时注解

编译时注解的核心依赖APT(Annotation Processing Tools)实现，对应的处理流程为：

- 在某些代码元素上（如类型、函数、字段等）添加注解
- 编译时编译器会检查AbstractProcessor的子类
- 然后将添加了注解的所有元素都传递到该类的process函数中，使得开发人员可以在编译器进行相应的处理，比如动态生成代码

# 引入依赖

```xml
<dependency>
    <groupId>com.google.auto.service</groupId>
    <artifactId>auto-service</artifactId>
    <version>1.0-rc7</version>
</dependency>
```

# 创建一个注解

```java
package org.m1;

public @interface M1A {
}
```

# 创建对应的注解处理器

注意：不要将AbstractProcessor和使用该AbstractProcessor的类写在同一个项目中，会因为AbstractProcessor没有预编译导致报错

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

@AutoService(Processor.class)
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
        } catch (IOException e) {
        }
        return true;
    }
}
```

# 使用注解

```java
package org.example;

import org.m1.M1A;

public class Test {

    @M1A
    public void t() {

    }
}
```

# 使用动态生成的类

```java
package org.example;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class App {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
        Class<?> aClass = Class.forName("org.ex.m1.GeneratedClass");
        Method getMessage = aClass.getMethod("getMessage");
        Constructor<?> constructor = aClass.getConstructor();
        Object o = constructor.newInstance();
        System.out.println(getMessage.invoke(o));
    }
}
```

# 编译

编译器会缓存上一次生成的类文件，所以需要每次都mvn clean

mvn clean -> mvn install -> 运行main

在target目录下就会自动生成一个org.ex.m1.GeneratedClass类
