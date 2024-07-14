# 字符串

## 拼接

```go
str1 := "a"
// 拼接字符串
str2 := str1 + "b"
// 拼接其它类型
str3 := str1 + strconv.Itoa(100)
```

## 比较

```go
str1 := "str1"
str2 := "str2"
// false
fmt.Println(str1 == str2)
// false
fmt.Println(str1 > str2)
```

## contains

```go
str1 := "str1"
// true
fmt.Println(strings.Contains(str1, "1"))
```

## split

```go
str1 := "str1,str2"
// [str1 str2]
fmt.Println(strings.Split(str1, ","))
```

## startsWith

```go
str1 := "str1234567890"
// true
fmt.Println(strings.HasPrefix(str1, "str"))
```

## endsWith

```go
str1 := "str1234567890"
// true
fmt.Println(strings.HasSuffix(str1, "0"))
```

## indexOf

```go
str1 := "str1234567890"
// 3
fmt.Println(strings.Index(str1, "123"))
```

## replace

```go
str1 := "str1234567890"
// str---4567890
// 最后一个参数表示替换几个, 负数表示全部替换
fmt.Println(strings.Replace(str1, "123", "---", -1))
```

## trim

```go
str1 := "   s t r   "
// s t r
fmt.Println(strings.Trim(str1, " "))
```

## 大小写转换

```go
// test
fmt.Println(strings.ToLower("TEST"))
// TEST
fmt.Println(strings.ToUpper("test"))
```

## string builder

```go
username := "test"
age := 10
var sb strings.Builder
sb.WriteString("username=")
sb.WriteString(username)
sb.WriteString(", ")
sb.WriteString("age=")
sb.WriteString(strconv.Itoa(age))

str1 := sb.String()
```
