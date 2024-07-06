# Gradle Wrapper

Gradle Wrapper（通常简称为 Gradle 包装器或 Wrapper）是 Gradle 提供的一个工具, 它允许开发者在没有预先安装 Gradle 的情况下构建项目。Gradle Wrapper 包含两个主要的文件: 

1. gradlew: 这是一个用于 Unix-based 系统的 shell 脚本, 位于项目根目录下
2. gradlew.bat: 这是一个用于 Windows 系统的批处理文件, 也位于项目根目录下

这两个脚本封装了 Gradle 构建过程, 使得开发者可以通过执行这些脚本来下载并运行 Gradle, 而不需要手动安装 Gradle 本身。这样, 团队成员和持续集成（CI）系统可以确保使用相同的 Gradle 版本来构建项目, 从而避免因 Gradle 版本不一致而导致的构建问题。

## 生成 Gradle Wrapper

```sh
gradle wrapper
```

生成的目录结构:

```
.
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
└── gradlew.bat
```

- gradle-wrapper.jar: Gradle Wrapper 的核心 JAR 文件, 它包含了用于运行 Gradle 构建的代码。当运行 gradlew 或 gradlew.bat 脚本时, 实际上是这个 JAR 在负责下载实际的 Gradle（如果本地没有缓存该版本的 Gradle）, 并执行构建脚本
- gradle-wrapper.properties: 这是一个配置文件, 它指定了项目需要使用的 Gradle 版本。它还可能包含其他配置, 比如 Gradle 的下载地址
- gradlew: 封装了执行 Gradle Wrapper 的命令。它允许开发者通过在终端中运行 `./gradlew` 来执行 Gradle 构建任务, 而不需要手动调用 gradle-wrapper.jar
- gradlew.bat: 专门为 Windows 系统准备的批处理脚本, 作用与 gradlew 相同

## gradle-wrapper.properties 文件

```sh
distributionUrl=https\://services.gradle.org/distributions/gradle-8.7-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
```

### distributionUrl

指定 gradle 的下载地址, 构建时会先去这个地址下载 gradle。

也可以指定 gradle 的本地路径, 来避免联网下载, 比如:

```sh
distributionUrl=file:///home/software/gradle-8.7-bin.zip
```

### zipStoreBase 和 zipStorePath

共同组成 gradle 的下载位置, 格式: `distributionBase/distributionPath`。

GRADLE_USER_HOME 是环境变量, 如果没有设置, 默认是`~/.gradle`。

例子中的 `gradle-8.7-bin.zip` 会被下载到 `~/.gradle/wrapper/dists` 目录下。

### distributionBase 和 distributionPath

共同组成 gradle 的解压位置, 格式: `distributionBase/distributionPath`。构建时

例子中的 `gradle-8.7-bin.zip` 下载后会被解压到 `~/.gradle/wrapper/dists` 目录下。

目录结构如下:

```
~/.gradle/wrapper/dists
└── gradle-8.7-bin
    └── af3un6e4ivqgjcdo5lfa5efog
        ├── gradle-8.7
        │   ├── LICENSE
        │   ├── NOTICE
        │   ├── README
        │   ├── bin
        │   │   ├── gradle
        │   │   └── gradle.bat
        │   ├── init.d
        │   │   └── readme.txt
        │   └── lib
        │       ├── ...
        ├── gradle-8.7-bin.zip.lck
        └── gradle-8.7-bin.zip.ok
```

`af3un6e4ivqgjcdo5lfa5efog` 是根据 distributionUrl 路径字符串计算 md5 值得来的。

在构建时, 如果 distributionUrl, distributionBase 和 distributionPath 都相同, 就不会再重新下载 gradle, 而是直接使用现有的。

## 使用 wrapper 构建

```sh
./gradlew build
```

## 升级使用的 gradle 版本

有两种方法: 

1. 更改 gradle-wrapper.properties 文件中的 distributionUrl 属性
2. 使用命令 `gradlew wrap --gradle-version 新版本号`
