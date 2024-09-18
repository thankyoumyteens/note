# panic

panic 是 Go 语言中的一个内置函数，它终止正常的控制流程并导致程序停止执行。

```go
package main

import (
	"fmt"
)

func main() {
	fmt.Println("123")
	panic("终止程序")
	fmt.Println("不会执行到这里")
}
```
