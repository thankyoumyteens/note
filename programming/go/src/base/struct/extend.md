# 实现继承

通过嵌套结构体实现继承

```go
package main

import "fmt"

type Parent1 struct {
	Name string
}

type Parent2 struct {
	Age string
}

type Child struct {
	Parent1 // 不指定名称
	Parent2
}

func main() {
	m1 := &Child{}
	m1.Name = "hello" // 也可以写成 m1.Parent1.Name
	m1.Age = "10"
	fmt.Println(m1.Name, m1.Age)
}
```
