# 编译 OpenJDK

环境：ubuntu14.04

```sh
sudo chmod 777 configure
./configure --with-target-bits=64 --with-debug-level=slowdebug
make
```

## 验证

```sh
build/linux-x86_64-normal-server-slowdebug/jdk/bin/java -version
```
