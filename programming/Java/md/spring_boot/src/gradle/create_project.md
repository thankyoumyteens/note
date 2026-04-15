# 项目搭建(JDK25)

### 1. 环境依赖要求

- JDK: Java 25 (推荐使用 LTS 版本或最新的 GA 版本)。
- Gradle: 需要 8.14 或 9.x 以上版本，以全面支持 Java 25 的字节码。
- Jakarta EE: 4.0 版本要求 Jakarta EE 11。

### 2. 目录结构搭建

```
spring-boot-demo-25/
├── build.gradle
├── settings.gradle
└── src/
    └── main/
        ├── java/
        │   └── com/example/demo/
        │       └── MySpringBootApplication.java
        └── resources/
            └── application.properties
```

手动创建以上目录结构（或者在 IDEA 中新建一个空的 Gradle 项目）：

```sh
mkdir spring-boot-demo-25
cd spring-boot-demo-25
touch build.gradle
touch settings.gradle
mkdir -p src/main/java/com/example/demo/
touch src/main/java/com/example/demo/MySpringBootApplication.java
mkdir -p src/main/resources/
touch src/main/resources/application.properties
```

### 3. settings.gradle

指定项目名称：

```grovy
rootProject.name = 'spring-boot-demo-25'
```

### 4. build.gradle

### 5. 生成特定版本的 Wrapper

为了生成 Wrapper，你的电脑上需要先有一个安装好的 Gradle：

```sh
brew install gradle
gradle -v
```

生成 Wrapper：

```sh
gradle wrapper --gradle-version 9.4.1 --distribution-type all
```

执行完成后，你会发现目录中多出了以下文件：

- gradlew (Unix/macOS 脚本)
- gradlew.bat (Windows 脚本)
- gradle/wrapper/gradle-wrapper.jar
- gradle/wrapper/gradle-wrapper.properties

### 6. 下载 Gradle 并运行项目

```sh
chmod +x gradlew
export GRADLE_OPTS="-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=7890 -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=7890 -Dsun.net.client.defaultConnectTimeout=300000 -Dsun.net.client.defaultReadTimeout=300000 -Djava.net.preferIPv4Stack=true"
./gradlew bootRun
```

