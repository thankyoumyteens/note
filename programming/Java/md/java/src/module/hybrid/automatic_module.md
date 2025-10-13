# 自动模块

模块不能读取类路径，所以将自己的代码转移到模块上之后, 不能访问类路径上的库。解决的办法是使用自动模块。

自动模块(Automatic Module)是指那些未包含 module-info.class 的传统 JAR 包，当它们被放入模块路径(`--module-path`)时，会被 Java 自动识别为 “自动模块”，从而可以被其他模块依赖。

自动模块是 Java 模块系统为了兼容传统非模块化 JAR 而设计的过渡机制。它允许模块化项目(含 module-info.java)依赖未模块化的老旧库，同时让非模块化 JAR 也能参与到模块系统中。

自动模块的核心特点:

- 来源：所有未模块化的 JAR(即没有 module-info.class 的传统 JAR)，只要被放在模块路径下，就会被自动转换为自动模块
- 模块名的确定：自动模块的名称由 JAR 文件名推导而来，规则如下：
  - 移除文件名中的 .jar 后缀
  - 替换文件名中的非字母数字字符(如 -、\_、.)为 .
  - 移除开头和结尾的 .，并合并连续的 .
  - 例如：jackson-databind-2.8.8.jar 会被识别为模块名 jackson.databind
- 导出与开放：自动模块会导出其所有包(即其他模块可以通过 requires 依赖它，并访问其所有公共类)，同时开放所有包(允许反射访问)。这是为了兼容传统 JAR 的使用方式(传统 JAR 没有模块边界限制)
- 依赖处理：自动模块会隐式依赖所有其他模块(包括平台模块和其他自动模块)，以确保兼容性(避免传统 JAR 因依赖缺失而报错)

### 1. 修改目录结构

```
.
├── mods
│   ├── jackson-annotations-2.8.8.jar
│   ├── jackson-core-2.8.8.jar
│   └── jackson-databind-2.8.8.jar
└── src
    └── demo
        ├── com
        │   └── example
        │       ├── Main.java
        │       └── Person.java
        └── module-info.java
```

### 2. module-info.java

```java
module demo {
    requires jackson.databind;
}
```

### 3. 编译

把 jackson 的 jar 包加入模块路径

```sh
javac -d target --module-path mods --module-source-path src -m demo
```

### 4. 运行

```sh
java --module-path mods:target -m demo/com.example.Main
```

### 5. 报错

```sh
Exception in thread "main" java.lang.reflect.InaccessibleObjectException: Unable to make public java.lang.String com.example.Person.getName() accessible: module demo does not "exports com.example" to module jackson.databind
```

Jackson Databind 使用反射来查看类的字段以便进行序列化。因此，Jackson Databind 需要访问 Person 类；否则，就无法使用反射来查看它的字段。为此，包含该类的包必须通被导出或开放(导出包可以反射公共元素，而开放包则允许进行深度反射)。

### 6. 开放反射权限

```java
module demo {
    requires jackson.databind;

    opens com.example;
}
```

### 7. 重新编译+运行
