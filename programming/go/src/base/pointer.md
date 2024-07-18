# 指针

区别于 C/C++中的指针，Go 语言中的指针不能进行偏移和运算。

go 中的指针只是用来实现按引用传值。

```go
package main

import "fmt"

func changeValue(a *int) {
    *a = *a + 10
}

func main() {
    a := 1
    changeValue(&a)
    fmt.Println(a) // 11

    p := &a
    *p = 2
    fmt.Println(a) // 2
}
```

## 结构体指针

结构体也是值传递的, 想按引用传递的话也需要指针。

```go
package main

import "fmt"

type person struct {
    id   int
    name string
    age  int
}

func changeValue(a *person) {
    // 语法糖, 等同于: (*a).age = 10
    a.age = 10
}

func main() {
    a := person{id: 1, name: "Alice", age: 20}
    changeValue(&a)
    fmt.Println(a) // 2
}
```
