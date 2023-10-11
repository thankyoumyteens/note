# 下载maven

```sh
cd ~/src_pack
wget https://repo.huaweicloud.com/apache/maven/maven-3/3.5.3/binaries/apache-maven-3.5.3-bin.tar.gz
tar -zxvf apache-maven-3.5.3-bin.tar.gz
```

# 配置环境变量

1. 打开配置文件
```sh
sudo vim /etc/profile
```

2. 在最后一行添加：
```conf
export PATH=/root/src_pack/apache-maven-3.5.3/bin:$PATH
```

3. 使环境变量生效
```sh
source /etc/profile
```

# 验证

```sh
mvn --help
```
