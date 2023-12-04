# 下载JDK 17

```sh
mkdir ~/jdk
cd ~/jdk
wget https://download.bell-sw.com/java/17.0.9+11/bellsoft-jdk17.0.9+11-linux-amd64.tar.gz
tar -zxvf bellsoft-jdk17.0.9+11-linux-amd64.tar.gz
```

# 配置环境变量

1. 打开配置文件
```sh
sudo vim /etc/profile
```

2. 在最后一行添加: 
```conf
export JAVA_HOME=/root/src_pack/dragonwell-17.0.8.0.8+7-GA
export PATH=$JAVA_HOME/bin:$PATH
```

3. 使环境变量生效
```sh
source /etc/profile
```

# 验证

```sh
java -version
```
