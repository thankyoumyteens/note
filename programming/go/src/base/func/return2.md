# 返回多个值

```go
package main

import "fmt"

func getInfo() (string, int) {
	return "zhangsan", 10
}

func main() {
	name, age := getInfo()
	fmt.Println(name, age)
}
```
