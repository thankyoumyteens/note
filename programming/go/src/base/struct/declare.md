# 创建结构体

```go
type 结构体名 struct {
    字段名1 数据类型1,
    字段名2 数据类型2,
    ...
}
```

要访问结构体的数据字段，可使用点表示法：`结构体变量名.要访问的数据字段的名称`。

```go
package main

import "fmt"

type Student struct {
	name string
	age  int
}

func main() {
	var s Student
	s.name = "John"
	fmt.Println(s.name)
}
```

也可使用关键字 new 来创建结构体实例

```go
s := new(Student)
```

创建结构体实例时，可同时给字段赋值

```go
s := Student{name: "John", age: 25}
```
