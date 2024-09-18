# 通道作为函数参数

<- 位于关键字 chan 左边时，表示通道在函数内是只读的

```go
func wait(c <-chan string) {
	time.Sleep(5 * time.Second)
	c <- "继续执行" // 编译时报错
}
```

<- 位于关键字 chan 右边时，表示通道在函数内是只写的

```go
func wait(c chan<- string) {
	time.Sleep(5 * time.Second)
	c <- "继续执行"
}
```

没有指定 <- 时，表示通道是可读写的

```go
func wait(c chan string) {
	time.Sleep(5 * time.Second)
	c <- "继续执行"
}
```
