# 查找

## MatchString

MatchString 函数用来匹配子串

```go
re := regexp.MustCompile(`age:(\d{2})`)
// true
fmt.Println(re.MatchString("name:zhangsan,age:17"))
```

## FindString

FindString 用来返回第一个匹配的结果。如果没有匹配的字符串，那么它回返回一个空的字符串

```go
re := regexp.MustCompile(`age:(\d{2})`)
// age:17
fmt.Println(re.FindString("name:zhangsan,age:17"))
```

## FindAllString

FindAllString 函数返回所有匹配的切片

```go
re := regexp.MustCompile(`age:(\d{2})`)
// -1 表示搜索所有可能的匹配项
// [age:17]
fmt.Println(re.FindAllString("name:zhangsan,age:17"))
```
