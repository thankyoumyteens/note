# 安装 jdk

### 1. 下载:

```sh
wget https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.5%2B11/OpenJDK21U-jdk_x64_linux_hotspot_21.0.5_11.tar.gz
tar -zxvf OpenJDK21U-jdk_x64_linux_hotspot_21.0.5_11.tar.gz
```

### 2. 配置环境变量:

```sh
# 打开配置文件
sudo vim /etc/profile

# 在最后一行添加
export JAVA_HOME=/jdk/jdk-21.0.5+11
export PATH=$JAVA_HOME/bin:$PATH

# 使环境变量生效
source /etc/profile
```

### 3. 验证:

```sh
java -version
```
