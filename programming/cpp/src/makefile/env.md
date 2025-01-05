# 环境搭建

1. 安装 gnu make

```sh
# 安装路径: /opt/homebrew/Cellar/make/
brew install make
```

2. 安装 gcc

```sh
# 安装路径: /opt/homebrew/Cellar/gcc
brew install gcc
```

3. 查看 make 版本

```sh
# gnu make在linux下一般是叫make
# 但是如果是在其他的unix系统下, 因为有一个原生的make
# gnu make就改个名字叫gmake了
gmake --version
```

4. 查看 gcc 版本

```sh
/opt/homebrew/bin/gcc-14 -v
```
