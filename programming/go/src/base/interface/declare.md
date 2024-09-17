# 定义接口

接口指定了一个方法集, 它描述了方法集中的所有方法，但没有实现它们。

```go
type 接口名 interface {
    方法名1(参数列表1) 返回值1,
    方法名2(参数列表2) 返回值2,
    ...
}
```

只要方法的函数签名与接口中某个(或多个)方法要求的一致, 就算实现了接口。

```go
package main

import "fmt"

// 定义接口
type Robot interface {
	PowerOn() string
	PowerOff() string
}

type MK2000 struct {
	id string
}

// 实现Robot接口
func (m *MK2000) PowerOn() string {
	return m.id + " Power On"
}

func main() {
	m1 := MK2000{"MK2000-1"}
	m2 := MK2000{"MK2000-2"}

	fmt.Println(m1.PowerOn())
	fmt.Println(m2.PowerOn())
}
```

通过接口, Go 在不使用类和继承的情况下提供了类似于面向对象编程的功能。
