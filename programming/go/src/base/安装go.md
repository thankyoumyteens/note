# 安装 go

下载安装程序:

- [官方](https://go.dev/dl/)
- [镜像](https://mirrors.ustc.edu.cn/golang/)

## 设置国内代理

```sh
go env -w GOPROXY=https://goproxy.cn,direct
```

## vscode 环境配置

1. 扩展商店搜索安装: golang.go
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
git clone https://github.com/acroca/go-symbols.git
cd ..
cd cweill
git clone https://github.com/cweill/gotests.git
cd ..
cd derekparker
git clone https://github.com/derekparker/delve.git
cd ..
cd go-delve
git clone https://github.com/go-delve/delve.git
cd ..
cd josharian
git clone https://github.com/josharian/impl.git
cd ..
cd karrick
git clone https://github.com/karrick/godirwalk.git
cd ..
cd mdempsky
git clone https://github.com/mdempsky/gocode.git
cd ..
cd pkg
git clone https://github.com/pkg/errors.git
cd ..
cd ramya-rao-a
git clone https://github.com/ramya-rao-a/go-outline.git
cd ..
cd rogpeppe
git clone https://github.com/rogpeppe/godef.git
cd ..
cd sqs
git clone https://github.com/sqs/goreturns.git
cd ..
cd uudashr
git clone https://github.com/uudashr/gopkgs.git
cd ..
mkdir -p golang.org/x
cd golang.org/x
git clone https://github.com/golang/tools.git
git clone https://github.com/golang/lint.git

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
