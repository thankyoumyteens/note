# 断言类型转换

变量必须是接口类型。

写法 1

```go
转换后的变量 := 变量.(要转换的类型) // 如果断言失败则触发 panic
```

写法 2

```go
转换后的变量, 是否成功 := 变量.(要转换的类型) // 断言失败不会触发 panic
```

示例

```go
package main

import "fmt"

type A interface {
}

func main() {
	var a A
	format := a.(int) // panic: interface conversion: main.A is nil, not int
	fmt.Println(format)
}
```

## switch 使用断言

```go
package main

import "fmt"

type A interface {
	Do()
}

type AChild struct {
}

func (a *AChild) Do() {
	fmt.Println("A Do")
}

type BChild struct {
}

func (b *BChild) Do() {
	fmt.Println("B Do")
}

func testConvert(a A) {
	switch a.(type) {
	case *AChild: // 接口的值是引用, 所以需要用指针判断
		fmt.Println("AChild")
	case *BChild:
		fmt.Println("BChild")
	default:
		fmt.Println("default")
	}
}

func main() {
	testConvert(&AChild{})
}
```
