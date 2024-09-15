# 常量

常量指的是在整个程序生命周期内都不变的值。常量初始化后，可以引用它，但不能修改它。

```go
const 常量名 常量类型 = 常量值
```

常量类型可以省略。

```go
package main

import "fmt"

func main() {
	const a = 100
	fmt.Println(a)
}
```
