# 自动释放资源

defer 用于自动释放资源。

不使用 defer 的话:

```go
func main() {
    m1 := sync.Mutex{}
    m2 := sync.Mutex{}

    m1.Lock()
    m2.Lock()
    fmt.Println("加锁访问")
    m2.Unlock()
    m1.Unlock()
}
```

使用 defer:

```go
// defer后的语句会在函数return之后执行
// m2.Unlock()会先于m1.Unlock()执行
func main() {
    m1 := sync.Mutex{}
    m2 := sync.Mutex{}
    defer m1.Unlock()
    defer m2.Unlock()

    m1.Lock()
    m2.Lock()
    fmt.Println("加锁访问")
}
```
