# defer 语句

defer 能够在函数返回前执行另一个函数。

外部函数执行完毕后，按与 defer 语句出现顺序相反的顺序执行它们指定的函数:

```go
package main

import "fmt"

// 输出:
// 第1行
// 第2行
// 第3行
func main() {
	defer fmt.Println("第3行")
	defer fmt.Println("第2行")
	fmt.Println("第1行")
}
```
