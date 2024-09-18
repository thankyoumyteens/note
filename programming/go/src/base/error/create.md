# 创建错误

```go
package main

import (
	"errors"
	"fmt"
)

func main() {
	err := errors.New("这是一个错误")
	fmt.Println(err)
}
```
