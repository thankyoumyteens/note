# 字符串类型转换

strconv 包提供了一整套类型转换方法，可用于转换为字符串或将字符串转换为其他类型。

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// int转字符串
	fmt.Println(strconv.Itoa(100))
	// 字符串转int
	i, err := strconv.Atoi("100")
	fmt.Println(i, err)

	// bool转字符串
	fmt.Println(strconv.FormatBool(true))
	// 字符串转bool
	b, err := strconv.ParseBool("true")
	fmt.Println(b, err)
}
```
