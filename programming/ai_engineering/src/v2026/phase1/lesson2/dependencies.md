# 先加依赖

如果你用 Maven，确认 `pom.xml` 里有这些依赖：

```xml
<dependencies>
    <!-- Spring Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- WebClient 需要 WebFlux 依赖 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>

    <!-- 配置属性绑定 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-configuration-processor</artifactId>
        <optional>true</optional>
    </dependency>

    <!-- Lombok 可选，不用也行 -->
</dependencies>
```

如果你已经有 `spring-boot-starter-web`，只需要额外加 `spring-boot-starter-webflux`。

## macOS 网络环境下可能出现 DNS 解析不符合系统配置的问题

如果使用 macOS 系统，在后面调用接口时可能会输出下面的警告：

```text
Unable to load io.netty.resolver.dns.macos.MacOSDnsServerAddressStreamProvider
```

这条日志不是业务异常，它的意思是：你在 macOS 上使用 Spring WebClient / Reactor Netty 时，Netty 尝试加载 macOS 专用 DNS native resolver，但当前 classpath 里没有对应 native 依赖，于是 fallback 到系统默认 DNS 解析。Netty / Reactor Netty 相关 issue 里也长期记录过这个现象，常见解决方式是补充 netty-resolver-dns-native-macos 依赖。

### 推荐修复方式：加 Netty macOS native resolver

在 `pom.xml` 里加这个依赖：

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-resolver-dns-native-macos</artifactId>
    <classifier>osx-aarch_64</classifier>
</dependency>
```

如果你是 Intel Mac，用：

```xml
<dependency>
    <groupId>io.netty</groupId>
    <artifactId>netty-resolver-dns-native-macos</artifactId>
    <classifier>osx-x86_64</classifier>
</dependency>
```

不要手写版本号，让 Spring Boot 的 dependency management 接管 Netty 版本。这样可以避免 Netty 版本和 Spring Boot 管理版本不一致。
