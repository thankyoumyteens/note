# 获取变量的数据类型

可使用标准库中的 reflect 包检查数据类型

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	var a int = 10
	// 输出: int
	fmt.Println(reflect.TypeOf(a))
}
```
