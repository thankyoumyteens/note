# 日期加减

```go
t := time.Now()

// 加1年
fmt.Println(t.AddDate(1, 0, 0))
// 减1年
fmt.Println(t.AddDate(-1, 0, 0))

// 加1月
fmt.Println(t.AddDate(0, 1, 0))
// 减1月
fmt.Println(t.AddDate(0, -1, 0))

// 加1天
fmt.Println(t.AddDate(0, 0, 1))
// 减1天
fmt.Println(t.AddDate(0, 0, -1))

// 加1小时
fmt.Println(t.Add(1 * time.Hour))
// 减1小时
fmt.Println(t.Add(-1 * time.Hour))

// 加1分钟
fmt.Println(t.Add(1 * time.Minute))
// 减1分钟
fmt.Println(t.Add(-1 * time.Minute))

// 加1秒
fmt.Println(t.Add(1 * time.Second))
// 减1秒
fmt.Println(t.Add(-1 * time.Second))
```
