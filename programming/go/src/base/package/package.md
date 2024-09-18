# 包

Go 程序以 package 语句打头。main 包是一种特殊的包，其特殊之处在于不能导入。对 main 包的唯一要求是，必须声明一个 main 函数，这个函数不接受任何参数且不返回任何值。简而言之，main 包是程序的入口。

在 main 包中，可使用 import 声明来导入其他包。导入包后，就可使用其中被导出的（即公有的）标识符。在 Go 语言中，标识符可以是变量、常量、类型、函数或方法。这让包能够通过接口提供各种功能。

```go
package main

import (
	"fmt"
	// 导入 math 包
	"math"
)

func main() {
	// 访问 math 包中的 Pi 常量
	fmt.Println(math.Pi)
}
```
