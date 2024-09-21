# 日期格式化

go 没有 `yyyy-MM-dd HH:mm:ss` 格式的操作，而是将其定义为 golang 的诞生时间, 很抽象。

`2006-01-02 15:04:05` 等价于 `yyyy-MM-dd HH:mm:ss`。

```go
now := time.Now()
fmt.Println(now.Format("2006-01-02 15:04:05"))
```
