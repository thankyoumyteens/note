# 运行 go 程序

## 初始化

```sh
mkdir test
cd test
# go mod init 后面的名称要和文件夹名一致
go mod init test
```

## 创建 do_say.go

```sh
mkdir say_hello
cd say_hello
touch do_say.go
```

do_say.go 文件内容如下：

```go
// 包名
package say_hello

import "fmt"
// 导出函数
func SayHello() {
    fmt.Println("Hello World!")
}
```

## 创建 hello.go

```sh
touch hello.go
```

hello.go 文件内容如下：

```go
package main

// 导入 say_hello 包
import (
	"test/say_hello"
)

// 程序入口
func main() {
    // 调用 do_say.go 中的 SayHello 函数
    // 需要用包名调用
    say_hello.SayHello()
}
```

## 目录结构

```
test/
├── go.mod
├── say_hello/
│   └── do_say.go
└── hello.go
```

## 运行程序

```sh
go run hello.go
```
