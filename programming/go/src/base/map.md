# map

```go
// key是string, value是int
var m1 = map[string]int{
    "k1": 1,
    "k2": 2,
}
// 使用前必须初始化
m1["k1"] = 0
fmt.Println(m1["k1"])
```

## 初始化

```go
// 方式1
var m1 = map[string]int{
    "k1": 1,
    "k2": 2,
}

// 方式2
var m1 = make(map[string]int)
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

## 删除

```go
var m1 = make(map[string]int)

delete(m1, "k1")
```
