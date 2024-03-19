# 安装 7-zip

下载：

[7z2301-mac.tar.xz](https://www.7-zip.org/a/7z2301-mac.tar.xz)

解压

```sh
mkdir 7z2301
tar -xvf 7z2301-mac.tar.xz -C 7z2301/
```

## 配置环境变量

1. 打开配置文件

```sh
vim ~/.zshrc
```

2. 在最后一行添加:

```conf
export PATH=/Users/walter/walter/software/7z2301:$PATH
```

3. 使环境变量生效

```sh
source ~/.zshrc
```

## 验证

```sh
7zz -h
```
