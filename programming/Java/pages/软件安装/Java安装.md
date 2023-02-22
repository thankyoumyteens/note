下载
```
wget https://github.com/alibaba/dragonwell8/releases/download/dragonwell-8.11.12_jdk8u332-ga/Alibaba_Dragonwell_8.11.12_x64_linux.tar.gz
tar -zxvf Alibaba_Dragonwell_8.11.12_x64_linux.tar.gz
```

编辑
```
sudo vim /etc/profile
```

输入内容
```conf
export JAVA_HOME=/home/walter/dragonwell-8.11.12
export PATH=$JAVA_HOME/bin:$PATH
```

生效
```
source /etc/profile
```
