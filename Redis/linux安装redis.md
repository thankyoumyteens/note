# ubuntu 源码安装redis

安装基本的编译工具
```
sudo apt install build-essential tcl
```

下载Redis源代码
```
curl -O http://download.redis.io/redis-stable.tar.gz
```

解压tar包
```
tar xzvf redis-stable.tar.gz
```

编译安装
```
cd redis-stable
make
make test
sudo make install
```
