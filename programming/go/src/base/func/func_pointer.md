# 将函数作为值传递

Go 将函数视为一种类型，因此可将函数赋给变量，以后再通过变量来调用它们:

```go
package main

import "fmt"

func main() {
	f := func() {
		fmt.Println("Hello, World!")
	}
	f()
}
```

函数也可以作为另一个函数的参数:

```go
package main

import "fmt"

// anotherFunc变量可以接受两个int参数, 1个int返回值的函数
func callAnotherFunc(anotherFunc func(int, int) int) {
	fmt.Println(anotherFunc(1, 1))
}

func main() {
	add := func(a int, b int) int {
		return a + b
	}
	callAnotherFunc(add)
}
```
