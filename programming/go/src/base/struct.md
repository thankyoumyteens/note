# 结构体

Go 语言中没有“类”的概念, 也不支持“类”的继承等面向对象的概念。

```go
type person struct {
    id   int
    name string
    age  int
}

func main() {
    var zhangsan person
    zhangsan.id = 1
    zhangsan.name = "zhangsan"
    zhangsan.age = 18
    fmt.Println(zhangsan)

    lisi := person{id: 2, name: "lisi", age: 18}
    fmt.Println(lisi)
}
```

## 匿名结构体

```go
var a struct {
    id   int
    name string
    age  int
}
a.name = "zhangsan"
fmt.Println(a)
```
