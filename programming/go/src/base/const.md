# 常量

定义常量的 2 种方式:

- `const 常量名 常量类型 = 常量值`
- `const 常量名 = 常量值`

```go
const a int = 1
const b = true
fmt.Println(a, b)
```

## 定义多个常量

```go
const (
    a = 1
    b = 2
)
fmt.Println(a, b)

const (
    c = "hello"
    d
)
// hello hello
fmt.Println(c, d)
```

## iota

iota 在 const 关键字内出现时将被重置为 0, const 中每新增一行常量声明将使 iota 加 1。

```go
// iota默认从0开始
const (
	a = iota
	b
	c
)
// 0 1 2
fmt.Println(a, b, c)

// 新的const, iota会重置为0
// 改变iota的初始值
const (
	d = iota + 100
	e
)
// 100 101
fmt.Println(d, e)

// 被其他类型中断, iota也会继续增加
const (
	f = iota + 1
	g
	h = "hello"
	i
	j
	k = iota
)
// 1 2 hello hello hello 5
fmt.Println(f, g, h, i, j, k)
```
