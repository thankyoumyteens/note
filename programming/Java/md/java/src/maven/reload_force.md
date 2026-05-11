# 强制重新下载依赖

```
org.springframework.boot:spring-boot-starter-tomcat:jar:3.5.14 failed to transfer from https://repo.maven.apache.org/maven2 during a previous attempt. This failure was cached in the local repository and resolution is not reattempted until the update interval of central has elapsed or updates are forced. Original error: Could not transfer artifact org.springframework.boot:spring-boot-starter-tomcat:jar:3.5.14 from/to central (https://repo.maven.apache.org/maven2): Remote host terminated the handshake

Try to run Maven import with -U flag (force update snapshots)
```

Maven 缓存失败结果的原因是：它会在本地仓库里写入一个 .lastUpdated 文件，表示“这个 artifact 刚刚尝试下载失败过”，然后在一定时间内不再重复访问远程仓库，避免频繁打爆仓库或代理。

## 方案 1：强制重新下载依赖

在项目根目录执行：

```sh
mvn -U clean install
```

-U 会强制 Maven 重新检查远程仓库，通常可以绕过之前失败留下的 .lastUpdated 缓存。

## 方案 2：删除所有失败缓存文件

```sh
find ~/.m2/repository -name "*.lastUpdated" -delete
```
