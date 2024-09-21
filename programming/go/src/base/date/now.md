# 获取日期

## 当前时间

```go
now := time.Now()
fmt.Println(now)

fmt.Println(now.Year())
fmt.Println(int(now.Month()))
fmt.Println(now.Day())
fmt.Println(now.Hour())
fmt.Println(now.Minute())
fmt.Println(now.Second())
```

## 时间戳

```go
now := time.Now().Unix()
```

## 指定时间

```go
now := time.Date(2020, 1, 1, 10, 01, 01, 0, time.UTC)
// 2020-01-01 10:01:01 +0000 UTC
fmt.Println(now)
```
