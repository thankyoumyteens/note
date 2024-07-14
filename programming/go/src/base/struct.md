# 结构体

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
