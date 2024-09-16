# 数组

```go
var 数组名 [数组长度]数据类型
```

使用索引访问数组的元素:

```go
package main

import "fmt"

func main() {
	var arr [5]int
	arr[0] = 1
	arr[1] = 2
	fmt.Println(arr[0])
}
```
