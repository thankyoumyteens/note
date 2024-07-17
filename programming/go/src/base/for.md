# 循环

go 中只有 for 循环。

## for 循环

```go
for i := 0; i < 3; i++ {
    fmt.Printf("%d ", i)
}
// 输出: 0 1 2
```

## while 循环

```go
i := 0
for i < 3 {
    fmt.Printf("%d ", i)
    i++
}
```

## while(true)

```go
for {
    fmt.Printf("1")
}
```

## for range 循环

for range 循环可以对数组、切片、链表、字典、集合、字符串等数据类型进行遍历。

```go
// 切片
s := []int{1, 2, 3}
for i, v := range s {
    fmt.Printf("index: %d, value: %d\n", i, v)
}
// index: 0, value: 1
// index: 1, value: 2
// index: 2, value: 3

// 字典
m := map[string]int{"one": 1, "two": 2, "three": 3}
for k, v := range m {
    fmt.Printf("key: %s, value: %d\n", k, v)
}
// key: one, value: 1
// key: two, value: 2
// key: three, value: 3
```
