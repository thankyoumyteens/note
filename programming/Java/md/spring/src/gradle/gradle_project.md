# Gradle 项目结构

一个典型的 Gradle 项目结构可能如下所示: 

```
my-project/
├── build.gradle
├── settings.gradle
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       └── MyApp.java
│   │   └── resources/
│   └── test/
│       ├── java/
│       └── resources/
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradle.properties
├── build/
├── lib/
├── scripts/
├── docs/
└── config/
```

1. **项目根目录**: 这是包含整个项目的顶层目录
2. **build.gradle**: 位于项目根目录下, 是主构建脚本文件, 定义了整个项目的构建配置, 包括依赖、插件、任务等
3. **settings.gradle**: 同样位于项目根目录下, 是设置脚本文件, 用于定义项目的子模块（subprojects）和项目之间的关系
4. **src**: 源代码目录, 通常包括以下子目录: 
   - **main**: 包含主要的源代码。
     - **java**: 存放 Java 源文件
     - **resources**: 存放资源文件, 如配置文件、属性文件等
   - **test**: 包含测试代码
     - **java**: 存放 Java 测试源文件
     - **resources**: 存放测试资源文件
5. **gradle**: 可能包含自定义的 Gradle 脚本或配置文件, 如初始化脚本或 Gradle Wrapper 配置
6. **gradle.properties**: 位于项目根目录或用户的 Gradle 缓存目录下, 用于配置 Gradle 本身的一些属性, 如 JVM 参数、并行构建等
7. **build**: 这是构建输出目录, 通常不在版本控制中。它包含构建生成的文件, 如编译后的类文件、JAR 文件等。这个目录由 `build.gradle` 中的 `buildDir` 属性指定
8. **lib**: 可能包含项目依赖的库文件, 尽管通常依赖是通过 build script 动态下载和管理的
9. **scripts**: 可能包含一些用于自动化或其他目的的脚本文件
10. **docs**: 项目文档
11. **config**: 配置文件, 可能包括数据库配置、应用服务器配置等
