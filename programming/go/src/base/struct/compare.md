# 比较结构体

对于类型相同的结构体, 要判断两个结构体是否相等, 可使用 `==`, 要判断它们是否不等, 可使用 `!=`。

```go
package main

import "fmt"

type Student struct {
	name string
	age  int
}

func main() {
	s1 := Student{
		name: "Naveen",
		age:  10,
	}
	s2 := Student{
		name: "Naveen",
		age:  10,
	}
	fmt.Println(s1 == s2) // true
}
```

不能对两个类型不同的结构体进行比较, 否则将导致编译错误。
