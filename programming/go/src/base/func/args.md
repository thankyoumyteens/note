# 可变数量的参数

```go
package main

import (
	"fmt"
)

// 变量numbers是一个包含所有参数的切片
func sum(numbers ...int) int {
	total := 0
	for _, number := range numbers {
		total += number
	}
	return total
}
func main() {
	result1 := sum(1, 2, 3, 4, 5)
	fmt.Println(result1)

	numberList := []int{1, 2, 3, 4, 5}
	// 如果切片已经存在，要使用...语法糖来将切片中的元素分开传递给函数
	result2 := sum(numberList...)
	fmt.Println(result2)
}
```
