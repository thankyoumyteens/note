# 运行 go 程序

1. 初始化

```sh
mkdir test
cd test
# go mod init 模块名
go mod init hello_world
# 程序入口
touch hello.go

```

2. hello.go 内容

```go
// 包名
package main

// 标准库
import "fmt"

// 程序入口
func main() {
    fmt.Println("Hello World!")
}
```

3. 运行

```sh
go run hello.go
```
