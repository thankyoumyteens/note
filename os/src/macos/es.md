# ElastiSearch

### 1. 打开下载页

[https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)

### 2. 下载对应版本

[elasticsearch-9.3.0-darwin-aarch64.tar.gz](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.3.0-darwin-aarch64.tar.gz)

### 3. 解压

```sh
tar -zxvf elasticsearch-9.3.0-darwin-aarch64.tar.gz
```

### 4. 运行

```sh
vim bin/elasticsearch

JAVA="/Users/walter/walter/jdk/jdk-17.0.10.jdk/bin/java"
```

```sh
cd ./elasticsearch-9.3.0
bin/elasticsearch
```

终端中会输出登录密码等信息

访问 [https://localhost:9200](https://localhost:9200)

注意: Elasticsearch 8+ 默认会启用安全和 https，并在第一次启动时生成一个 elastic 超级用户的密码，通常会在日志里给出。

## 重置 elastic 用户的密码

### 1. 先运行 Elasticsearch

### 2. 在一个新的终端窗口执行

```sh
cd /Users/walter/walter/software/elasticsearch-9.3.0
bin/elasticsearch-reset-password -u elastic
```

### 3. 输入 y 直接生成一个新密码

## 报错

### "jdk.app" Not Opened, Apple could not verify "jdk.app" is free of malware that may harm your Mac or compromise your privacy.

```sh
xattr -d com.apple.quarantine /Users/walter/walter/software/elasticsearch-9.3.0/jdk.app
bin/elasticsearch
```
