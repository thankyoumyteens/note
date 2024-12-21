# 安装 jdk

### 1. 下载:

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/x64/linux/OpenJDK21U-jdk_x64_linux_hotspot_21.0.5_11.tar.gz
tar -zxvf OpenJDK21U-jdk_x64_linux_hotspot_21.0.5_11.tar.gz

wget https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/aarch64/linux/OpenJDK21U-jdk_aarch64_linux_hotspot_21.0.5_11.tar.gz
tar -zxvf OpenJDK21U-jdk_aarch64_linux_hotspot_21.0.5_11.tar.gz

sudo mkdir /jdk
sudo mv jdk-21.0.5+11/ /jdk/jdk-21.0.5+11/
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
