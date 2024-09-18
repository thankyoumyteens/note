# 读取命令行参数

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println(os.Args[0])

	for index, arg := range os.Args {
		fmt.Println(index, arg)
	}
}
```
