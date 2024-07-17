# map

方式 1

```go
// var 变量名 = map[key的类型]value的类型{
//     key1: value1 // 初始化值1
//     key2: value2 // 初始化值2
// }
var m1 = map[string]int{
    "k1": 1,
    "k2": 2,
}
```

方式 2

```go
// var 变量名 = make(map[key的类型]value的类型, 初始容量)
var m2 = make(map[string]int, 10)
```

## map 的基本使用

```go
var m = make(map[string]int)
// 新增/修改
m["k1"] = 100
m["k2"] = 200
// 删除
delete(m, "k1")
// 读取
fmt.Println(m["k2"])
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
