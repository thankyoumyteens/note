# map

- `var 变量名 = map[key的类型]value的类型{初始值}`
- `var 变量名 = make(map[key的类型]value的类型)`

```go
// 方式1
// var 变量名 = map[key的类型]value的类型{
//     key1: value1 // 初始化值1
//     key2: value2 // 初始化值2
// }
var m1 = map[string]int{
    "k1": 1,
    "k2": 2,
}
// 访问k1的value
fmt.Println(m1["k1"])

// 方式2
var m2 = make(map[string]int)
m2["k3"] = 100
```

## contains

```go
var m1 = make(map[string]int)
m1["k1"] = 0
v, contain := m1["k1"]
if contain {
    fmt.Println(v)
}

// 紧凑写法
var m1 = make(map[string]int)
m1["k1"] = 0
if v, contain := m1["k1"]; contain {
    fmt.Println(v)
}
```

## 删除元素

```go
var m1 = make(map[string]int)

delete(m1, "k1")
```
