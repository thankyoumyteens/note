# 安装 go

下载安装程序:

- [官方](https://go.dev/dl/)
- [镜像](https://mirrors.ustc.edu.cn/golang/)

## mac 安装

1. 下载 `go1.23rc1.darwin-arm64.pkg`
2. 下载完成后，直接点击安装包进行安装，默认会安装到 `/usr/local/go` 文件夹下
3. 安装完成后，打开 Terminal，输入 `go version`

或者

1. 下载 `go1.23rc1.darwin-arm64.tar.gz` 解压
2. 配置环境变量

## 设置国内源

```sh
# 七牛云
go env -w GOPROXY=https://goproxy.cn,direct
# 官方cdn
go env -w  GOPROXY=https://goproxy.io,direct
```

## vscode 环境配置

1. 扩展商店搜索安装: `golang.go`

2. 安装 go 插件

```sh
# 使用 go env 找到GOPATH, 进入GOPATH目录
go_path="$(echo $(go env | grep GOPATH))"
echo "${go_path:11}"
cd "$(echo "${go_path:11}")/src"

# 下载源码
mkdir github.com
cd github.com
mkdir acroca cweill derekparker go-delve josharian karrick mdempsky pkg ramya-rao-a rogpeppe sqs uudashr
cd acroca
# git clone https://github.com/acroca/go-symbols.git
git clone https://gitee.com/hejuncheng1/go-symbols.git
cd ..
cd cweill
# git clone https://github.com/cweill/gotests.git
git clone https://gitee.com/cykon/gotests.git
cd ..
cd derekparker
# git clone https://github.com/derekparker/delve.git
git clone https://gitee.com/hubo/delve.git
cd ..
cd go-delve
# git clone https://github.com/go-delve/delve.git
git clone https://gitee.com/jiaojing119/delve.git
cd ..
cd josharian
# git clone https://github.com/josharian/impl.git
git clone https://gitee.com/cykon/impl.git
cd ..
cd karrick
# git clone https://github.com/karrick/godirwalk.git
git clone https://gitee.com/sandy1985/godirwalk.git
cd ..
cd mdempsky
# git clone https://github.com/mdempsky/gocode.git
git clone https://gitee.com/hejuncheng1/gocode.git
cd ..
cd pkg
# git clone https://github.com/pkg/errors.git
git clone https://gitee.com/hubo/errors.git
cd ..
cd ramya-rao-a
# git clone https://github.com/ramya-rao-a/go-outline.git
git clone https://gitee.com/Yed_kee/go-outline.git
cd ..
cd rogpeppe
# git clone https://github.com/rogpeppe/godef.git
git clone https://gitee.com/mrgrey/godef.git
cd ..
cd sqs
# git clone https://github.com/sqs/goreturns.git
git clone https://gitee.com/hejuncheng1/goreturns.git
cd ..
cd uudashr
# git clone https://github.com/uudashr/gopkgs.git
git clone https://gitee.com/HengliKuang/gopkgs.git
cd ..
mkdir -p golang.org/x
cd golang.org/x
# git clone https://github.com/golang/tools.git
git clone https://gitee.com/liu-jianle-China/tools.git
# git clone https://github.com/golang/lint.git
git clone https://gitee.com/rowlen/lint.git

# 设置国内代理
go env -w GOPROXY=https://goproxy.cn,direct

# 编译源码
cd "$(echo "${go_path:11}")/src"
go install github.com/mdempsky/gocode@latest
go install github.com/uudashr/gopkgs/cmd/gopkgs@latest
go install github.com/ramya-rao-a/go-outline@latest
go install github.com/acroca/go-symbols@latest
go install github.com/rogpeppe/godef@latest
go install github.com/sqs/goreturns@latest
go install github.com/derekparker/delve/cmd/dlv@latest
go install github.com/cweill/gotests@latest
go install github.com/josharian/impl@latest
go install golang.org/x/tools/cmd/guru@latest
go install golang.org/x/tools/cmd/gorename@latest
go install golang.org/x/lint/golint@latest
go install golang.org/x/tools/gopls@latest
```

3. 重启 vscode
