# 空接口

Go 语言的空接口 `interface{}` 类型很像 C 语言中的 `void*`, 该类型的变量可以容纳任何类型的值。

```go
package main

import (
	"fmt"
)

// 定义空接口
type A interface {
}

func main() {
	var a float32 = 1.1
	var b A
    // 空接口变量可以接收任意类型的数据, 相当于所有类型都实现了空接口
	b = a
	fmt.Println(b)
}
```
