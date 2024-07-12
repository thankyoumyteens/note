# 变量

定义变量的 3 种方式:

- `var 变量名 变量类型 = 变量值`, 变量值可选
- `var 变量名 = 变量值`
- `变量 := 变量值`, 这种方式只能在函数里用, 不能用于全局变量

## 匿名变量

在 go 中定义了变量就必须要使用, 如果不想使用这个变量, 可以使用匿名变量。

匿名变量使用下划线定义:

```go
func main() {
    // 不使用第二个返回值
    value, _ := getTwoValue()
    fmt.Println(value)
}
```

## 定义多个变量

```go
var a, b, c = "a", true, 100
fmt.Println(a, b, c)
var (
    d = 1
    e = 2
)
fmt.Println(d, e)
```
