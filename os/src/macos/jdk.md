# 安装 jdk

下载:

[bellsoft-jdk21.0.2+14-macos-aarch64.tar.gz](https://download.bell-sw.com/java/21.0.2+14/bellsoft-jdk21.0.2+14-macos-aarch64.tar.gz)

解压:

```sh
tar -xvf bellsoft-jdk21.0.2+14-macos-aarch64.tar
```

## 配置环境变量

1. 打开配置文件

```sh
vim ~/.zshrc
```

2. 在最后一行添加:

```conf
export JAVA_HOME=路径/jdk-21.0.2.jdk
export PATH=$JAVA_HOME/bin:$PATH
```

3. 使环境变量生效

```sh
source ~/.zshrc
```

## 验证

```sh
java -version
```

## 报错: 无法打开“java”，因为无法验证开发者。

1. 左上角 apple -> 系统设置 -> 隐私与安全性 -> 安全性
2. 已阻止使用“java”，因为来自身分不明的开发者。
3. 仍要打开
