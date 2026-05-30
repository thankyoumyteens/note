# 使用 uv 安装 python

## 安装最新版本的 Python

```sh
uv python install
```

安装完成后，uv 会把版本化的 Python 可执行文件放到 PATH 里，比如：

```
python3.13
```

## 安装指定版本

比如安装 Python 3.12：

```sh
uv python install 3.12
```

一次安装多个版本：

```sh
uv python install 3.11 3.12 3.13
```

## 查看已安装版本

```sh
uv python list
```
