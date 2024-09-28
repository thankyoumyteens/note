# 空接口

空接口类型，可以存储任意类型的数据。

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
