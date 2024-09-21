# 分组

```go
re := regexp.MustCompile(`age:(\d{2})`)
groups := re.FindStringSubmatch("name:zhangsan,age:17")
// 17
fmt.Println(groups[1])
```
