# 变量

定义变量的 3 种方式:

- `var 变量名 变量类型 = 变量值`, 变量值可选
  ```go
  var name string = "zhangsan"
  var age int
  ```
- `var 变量名 = 变量值`
  ```go
  var name = "zhangsan"
  ```
- `变量 := 变量值`, 这种方式只能声明函数里的局部变量, 不能用于全局变量
  ```go
  name := "zhangsan"
  ```

## 变量块

把同一类功能用到的变量定义在一起, 增强可读性:

```go
var (
    name string = "zhangsan"
    age  int    = 10
)
```

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
