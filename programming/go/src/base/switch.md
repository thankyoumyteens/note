# 分支

## if

if 的条件表达式不加括号。

```go
username := "test"
age := 10
if username == "test" && age > 10 {
	fmt.Printf("1")
} else if username == "test" && age > 5 {
	fmt.Printf("2")
} else {
	fmt.Printf("3")
}
```

## switch

case 执行完毕后不会紧接着执行下一个 case。

```go
x := 2

switch x {
case 1:
	fmt.Printf("1")
case 2:
	fmt.Printf("2")
case 3:
	fmt.Printf("3")
default:
	fmt.Printf("default")
}
// 输出: 2
```

## fallthrough

使用 fallthrough 会继续执行后面的 case 语句。

```go
x := 2
switch x {
case 1:
	fmt.Printf("1")
	fallthrough
case 2:
	fmt.Printf("2")
	fallthrough
case 3:
	fmt.Printf("3")
}
// 输出: 23
```
