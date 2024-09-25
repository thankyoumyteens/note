# Hello World

1. 配置环境变量:

```sh
export PATH=~/go/bin:$PATH
```

2. 安装

```sh
go install github.com/wailsapp/wails/v2/cmd/wails@latest
# 检查您是否安装了正确的依赖项
wails doctor
```

3. 创建项目

```sh
wails init -n myproject -t vue
cd myproject
# 运行
wails dev
```

## mac 上 wails dev 运行后不显示窗口

[使用 go 版本 1.23.1](https://github.com/wailsapp/wails/issues/3761)
