# 具名返回值

可在函数签名的返回值部分指定变量名, 在终止语句 return 前给具名变量进行赋值。

使用具名返回值时，无须显式地返回相应的变量。这被称为裸（naked）return 语句。

```go
package main

import "fmt"

func swap(a int, b int) (c int, d int) {
	c = b
	d = a
	return
}

func main() {
	a, b := swap(1, 2)
	fmt.Println(a, b)
}
```
