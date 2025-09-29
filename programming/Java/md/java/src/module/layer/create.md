# 创建新层

创建新层的完整流程可分为 5 步，核心是利用 ModuleLayer 和 Configuration 的 API 完成模块解析和层的实例化:

1. 确定父层: 新层必须有一个父层（通常是引导层或已存在的应用层），用于继承依赖
2. 定义模块来源: 通过 ModuleFinder 指定新层要加载的模块(如从指定目录、JAR 文件读取)
3. 解析模块依赖: 基于父层的配置和新模块来源，生成 Configuration(包含这些模块及其依赖模块的解析结果)
4. 创建类加载器: 为新层的模块创建专用的类加载器(通常以父层的类加载器为父，保证依赖可见性)
5. 实例化新层: 通过父层的 defineModulesWithOneLoader 或 defineModules 方法创建新层

## 示例

基于引导层（boot）创建一个新层，加载位于 /tmp/module1 目录下的 abc 模块。

### 1. 创建 abc 模块

目录结构

```sh
src/module1
├── aaa
│   └── bbb
│       └── Ccc.java
└── module-info.java
```

模块描述符

```java
module abc {
    // 导出包供外部使用
    exports aaa.bbb;
}
```

代码

```java
package aaa.bbb;

public class Ccc {
    public static void sayHello() {
        System.out.println("Hello from new layer!");
    }
}
```

### 2. 创建新层

目录结构

```sh
src/demo
├── com
│   └── example
│       └── CreateNewLayer.java
└── module-info.java
```

模块描述符

```java
module demo {
    // 无需依赖abc模块
}
```

代码

```java
package com.example;

import java.lang.module.Configuration;
import java.lang.module.ModuleFinder;
import java.net.URLClassLoader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Set;

public class CreateNewLayer {
    public static void main(String[] args) throws Exception {
        // 步骤1：确定父层（这里使用引导层）
        ModuleLayer parentLayer = ModuleLayer.boot();

        // 步骤2：定义新模块的来源（abc模块所在的目录）
        Path moduleDir = Paths.get("/tmp/module1"); // 模块存放目录
        ModuleFinder moduleFinder = ModuleFinder.of(moduleDir); // 从目录查找模块

        // 步骤3：解析模块依赖，生成配置
        // 基于父层的配置，解析新模块及其依赖
        Configuration parentConfig = parentLayer.configuration();
        Configuration newConfig = parentConfig.resolve(
                moduleFinder,      // 新模块的查找器
                ModuleFinder.of(), // 不额外添加其他模块
                Set.of("abc")      // 要加载的目标模块名
        );

        // 步骤4：为新层创建类加载器
        // 父加载器使用系统类加载器，确保能访问父层的类
        ClassLoader parentClassLoader = ClassLoader.getSystemClassLoader();
        // 新类加载器关联模块目录，用于加载新模块的类
        URLClassLoader newClassLoader = new URLClassLoader(
                new java.net.URL[]{moduleDir.toUri().toURL()},
                parentClassLoader
        );

        // 步骤5：基于父层、新配置和类加载器创建新层
        ModuleLayer newLayer = parentLayer.defineModulesWithOneLoader(
                newConfig,     // 新模块的配置
                newClassLoader // 新层的类加载器
        );

        // 验证新层是否创建成功
        System.out.println("新层是否包含目标模块：" +
                newLayer.modules().stream()
                        .anyMatch(m -> m.getName().equals("abc"))
        );

        // 使用新层中的类
        Class<?> helloClass = newLayer.findLoader("abc")
                .loadClass("aaa.bbb.Ccc");
        helloClass.getMethod("sayHello").invoke(null); // 调用静态方法
    }
}
```

### 3. 编译

```sh
javac -d out/module1 \
    src/module1/aaa/bbb/Ccc.java \
    src/module1/module-info.java

javac -d out/demo \
    src/demo/com/example/CreateNewLayer.java \
    src/demo/module-info.java
```

### 4. 运行

```sh
java --module-path out --module demo/com.example.CreateNewLayer
```
