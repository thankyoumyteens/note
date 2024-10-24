# 日期格式化

go 没有 `yyyy-MM-dd HH:mm:ss` 格式的操作，而是将其定义为 golang 的诞生时间, 很抽象。

`2006-01-02 15:04:05` 等价于 `yyyy-MM-dd HH:mm:ss`。

## 日期转字符串

```go
now := time.Now()
dateStr := now.Format("2006-01-02 15:04:05")
```

## 字符串转日期

```go
dateStr := "2020-10-01 19:25:00"
date, err := time.ParseInLocation("2006-01-02 15:04:05", dateStr, time.Local)
if err != nil {
    panic(err)
}
```
