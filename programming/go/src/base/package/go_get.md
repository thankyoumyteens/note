# 使用第三方包

要使用第三方包，必须先使用命令 go get 安装它。

```sh
# 在 go.mod 文件同级目录下执行
go get golang.org/x/example/hello
```

安装这个包后，就可导入它了(依赖的第三方包被下载到了 `$GOPATH/pkg/mod` 路径下)

```go
package main

import (
	"fmt"
	"golang.org/x/example/hello/reverse"
)

func main() {
	str := "Hello World!"
	fmt.Println(reverse.String(str))
}
```

通常，第三方包依赖于其他第三方包。命令 go get 会自动下载依赖的其它第三方包，无须手工安装每个包依赖的第三方包。
