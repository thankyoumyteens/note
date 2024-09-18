# 读取输入

```go
package main

import (
	"fmt"
)

func main() {
	var inputText string
	// 输入 a b c
	inputLength, err := fmt.Scan(&inputText)
	if err != nil {
		fmt.Println(err)
		return
	}
	// 输出 1
	fmt.Println(inputLength)
	// 输出 a
	fmt.Println(inputText)
}
```
