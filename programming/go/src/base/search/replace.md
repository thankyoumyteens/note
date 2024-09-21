# 替换

```go
re := regexp.MustCompile(`age:(\d{2})`)
// name:zhangsan,score:17
fmt.Println(re.ReplaceAllString("name:zhangsan,age:17", "score:$1"))
```
