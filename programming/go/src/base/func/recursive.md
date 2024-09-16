# 递归函数

```go
package main

import "fmt"

func calc(number int) int {
	if number <= 1 {
		return 1
	}
	return number * calc(number-1)
}

func main() {
	fmt.Println(calc(5))
}
```
