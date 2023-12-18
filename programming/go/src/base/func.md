# 函数

```go
func add(a int, b int) int {
	return a + b
}

// 函数可以返回多个值
func addWithError(a int, b int) (int, error) {
	return a + b, nil
}
func main() {
	fmt.Println(add(1, 1))
	fmt.Println(addWithError(1, 1))
}
```
