# 定义接口

接口指定了一个方法集, 它描述了方法集中的所有方法, 但没有实现它们。

```go
type 接口名 interface {
    方法名1(参数列表1) 返回值1,
    方法名2(参数列表2) 返回值2,
    ...
}
```

## 实现接口

如果任意一个类型的方法集是接口类型的方法集的超集, 那么这个类型就实现了此接口。

### 使用结构体实现接口

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

### 使用自定义类型实现接口

接口的实现不一定是结构体, 而可能是任意类型

```go
package main

import "fmt"

// 定义接口
type Robot interface {
	PowerOn() string
	PowerOff() string
}

type MK2000 []string

// 用切片实现Robot接口
func (m *MK2000) PowerOn() string {
	var s string
	for _, v := range *m {
		s += v + " "
	}
	return s + "PowerOn"
}

func main() {
	m1 := MK2000{"MK2000-1", "MK2000-1.1"}
	m1 = append(m1, "MK2000-1.2")
	m2 := MK2000{"MK2000-2"}

	fmt.Println(m1.PowerOn())
	fmt.Println(m2.PowerOn())
}
```
