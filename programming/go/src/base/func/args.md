# 可变数量的参数

```go
package main

import "fmt"

// 变量numbers是一个包含所有参数的切片
func sum(numbers ...int) int {
	total := 0
	for _, number := range numbers {
		total += number
	}
	return total
}

func main() {
	fmt.Println(sum(1, 2, 3, 4, 5))
}
```
