# 下载JDK 17

```sh
cd ~/src_pack
wget https://github.com/dragonwell-project/dragonwell17/releases/download/dragonwell-standard-17.0.8.0.8%2B7_jdk-17.0.8-ga/Alibaba_Dragonwell_Standard_17.0.8.0.8.7_x64_linux.tar.gz
tar -zxvf Alibaba_Dragonwell_Standard_17.0.8.0.8.7_x64_linux.tar.gz
```

# 配置环境变量

1. 打开配置文件
```sh
sudo vim /etc/profile
```

2. 在最后一行添加：
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
