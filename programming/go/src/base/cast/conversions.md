# 显式类型转换

```go
package main

import (
	"fmt"
)

func main() {
	var a float32 = 1.1
	fmt.Println(a)
	b := int32(a)
	fmt.Println(b)
}
```
