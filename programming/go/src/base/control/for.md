# for

```go
package main

func main() {
	i := 0
	for i < 5 {
		println("Hello, World!")
		i++
	}

	for i := 0; i < 5; i++ {
		println("Hello, World!")
	}
}
```

## range 子句

可使用包含 range 子句的 for 语句来遍历大多数数据结构，且无须知道数据结构的长度。

```go
package main

func main() {
	numbers := []int{1, 2, 3}
	for index, item := range numbers {
		println(index, item)
	}
}
```
