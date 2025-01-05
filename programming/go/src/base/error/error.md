# 错误处理

在 Go 语言中, 一种约定是在调用可能出现问题的方法或函数时, 返回一个类型为错误的值。这意味着如果出现问题, 函数通常不会引发异常, 而让调用者决定如何处理错误。

比如标准库中的 `os.ReadFile`:

```go
func ReadFile(name string) ([]byte, error)
```

它接受一个字符串参数, 并返回一个字节切片和一个 error。在调用 ReadFile 后, 通过检查 error 的值来判断是否出现了错误, 如果没有发生错误, 返回的 error 值将为 nil。

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	content, err := os.ReadFile("hello.txt")
	if err != nil {
		fmt.Println("读取失败", err)
		return
	}
	fmt.Println("文件内容: " + string(content))
}
```

## 错误类型

在 Go 语言中, 错误是一个值。标准库声明了接口 error:

```go
type error interface {
	Error() string
}
```
