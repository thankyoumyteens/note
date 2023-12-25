# 函数

```go
// 无返回值
func add1(a int, b int) {
	fmt.Println(a + b)
}

// 1个返回值
func add2(a int, b int) int {
	return a + b
}

// 多个返回值
func add3(a int, b int) (int, error) {
	return a + b, nil
}
func main() {
	add1(1, 1)
	fmt.Println(add2(1, 1))
	fmt.Println(add3(1, 1))
}
```
