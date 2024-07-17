# 函数

无返回值

```go
func add0(a int, b int) {
    fmt.Println(a + b)
}
// 相同类型的参数可以简写
func add1(a, b int) {
    fmt.Println(a + b)
}
```

一个返回值

```go
func add2(a, b int) int {
    return a + b
}
```

多个返回值

```go
func add3(a, b int) (int, error) {
    return a + b, nil
}
```

## 函数赋值给变量

```go
func add(a int, b int) {
    fmt.Println(a + b)
}

func main() {
    funcVar := add
    funcVar(1, 1)
}
```

## 函数作为参数传递

```go
func printInt(a int) {
    fmt.Println(a)
}

func listOperation(list []int, operation func(val int)) {
    for _, item := range list {
        operation(item)
    }
}

func main() {
    list := []int{1, 2, 3, 4, 5}
    listOperation(list, printInt)
}
```

## 匿名函数

```go
func listOperation(list []int, operation func(val int)) {
    for _, item := range list {
        operation(item)
    }
}

func main() {
    list := []int{1, 2, 3, 4, 5}
    listOperation(list, func(a int) {
        fmt.Println(a)
    })
}
```

## 函数作为返回值

```go
func printInt(a int) {
    fmt.Println(a)
}

func getOperation() func(val int) {
    return printInt
}

func main() {
    getOperation()(100)
}
```

## 闭包

go 支持类似 js 中的闭包:

```go
func getInc() func() int {
    a := 0
    return func() int {
        a += 1
        return a
    }
}

func main() {
    inc := getInc()
    // 1
    fmt.Println(inc())
    // 2
    fmt.Println(inc())
    // 3
    fmt.Println(inc())
}
```
