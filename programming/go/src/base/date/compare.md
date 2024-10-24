# 日期比较

```go
t1 := time.Now()
t2 := t1.AddDate(1, 0, 0)

fmt.Println(t1.Before(t2))
fmt.Println(t1.After(t2))
fmt.Println(t1.Equal(t2))
```
