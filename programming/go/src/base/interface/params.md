# 将接口作为参数传递

当一个结构体实现了一个接口的所有方法后, 就可以作为实现传递给以接口作为参数的方法中

```go
package main

import "fmt"

type Robot interface {
	PowerOn() string
	PowerOff() string
}

type MK2000 struct {
	id string
}

func (m *MK2000) PowerOff() string {
	return m.id + " Power Off"
}

func (m *MK2000) PowerOn() string {
	return m.id + " Power On"
}

// 将接口作为参数
func runRobot(instance Robot) {
	fmt.Println(instance.PowerOn())
	fmt.Println(instance.PowerOff())
}

func main() {
	m1 := MK2000{"MK2000-1"}
	m2 := MK2000{"MK2000-2"}

	runRobot(&m1) // MK2000必须实现接口的所有方法才能这么用
	runRobot(&m2)
}
```
