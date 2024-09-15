# 声明变量

```go
var 变量名 变量类型 = 变量值
```

变量类型和变量值可以同时存在, 但不能同时缺少。

## 快捷变量声明

可在一行内声明多个类型相同的变量并给它们赋值

```go
package main

import (
	"fmt"
)

func main() {
	var a, b, c int = 1, 2, 3
	fmt.Println(a, b, c)
}
```

## 变量块

把同一类功能用到的变量定义在一起, 增强可读性:

```go
package main

func main() {
	var (
		name string = "zhangsan"
		age  int    = 10
	)
	var (
		company string = "c1"
		salary  int    = 100
	)
	println(name, age, company, salary)
}
```
