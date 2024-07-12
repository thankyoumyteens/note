# 数组

- `var 变量名 [元素个数]类型`

```go
var arr0 [3]int
fmt.Println(arr0, arr0[0], arr0[1], arr0[2])
// 输出 [0 0 0] 0 0 0
```

奇葩问题

```go
var arr0 [3]int
var arr1 [4]int
arr0 = arr11
// 报错: cannot use arr1 (variable of type [4]int) as [3]int value in assignment
// 原因: [3]int 和 [4]int 是两种不同的数据类型
```

## 数组初始化

```go
// 初始化每个元素
arr := [3]string{"he", "is", "zhangsan"}

// 初始化索引为1的元素
arr1 := [3]string{1: "is"}

// 根据初始化的元素个数决定数组的长度
arr2 := [...]string{"he", "is", "zhangsan"}
```
