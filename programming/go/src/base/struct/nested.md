# 嵌套结构体

有时候, 数据结构需要包含多个层级。为建立较复杂的数据结构, 在一个结构体中嵌套另一个结构体的方式很有用。

```go
package main

import "fmt"

type Address struct {
	city, state string
}
type Student struct {
	name    string
	age     int
	address Address
}

func main() {
	s := Student{
		name: "Naveen",
		age:  10,
		address: Address{
			city:  "Chicago",
			state: "Illinois",
		},
	}
	fmt.Println(s.address.state)
}
```
