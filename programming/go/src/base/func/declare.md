# 函数的结构

```go
func 函数名(参数名1 参数类型1, 参数名2 参数类型2, ...) 返回值类型 {
    函数体
}
```

## 可变数量的参数

```go
package main

import "fmt"

// 变量numbers是一个包含所有参数的切片
func sum(numbers ...int) int {
	total := 0
	for _, number := range numbers {
		total += number
	}
	return total
}

func main() {
	fmt.Println(sum(1, 2, 3, 4, 5))
}
```

## 返回单个值

```go
func isBool(str string) bool {
	return str == "true" || str == "false"
}
```

## 返回多个值

```go
package main

import "fmt"

func getInfo() (string, int) {
	return "zhangsan", 10
}

func main() {
	name, age := getInfo()
	fmt.Println(name, age)
}
```

## 具名返回值

可在函数签名的返回值部分指定变量名, 在终止语句 return 前给具名变量进行赋值。

使用具名返回值时，无须显式地返回相应的变量。这被称为裸（naked）return 语句。

```go
package main

import "fmt"

func swap(a int, b int) (c int, d int) {
	c = b
	d = a
	return
}

func main() {
	a, b := swap(1, 2)
	fmt.Println(a, b)
}
```
