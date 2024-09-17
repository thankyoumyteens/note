# 字符串操作

## 拼接字符串

只能拼接类型为字符串的变量，如果将整数和字符串进行拼接将导致编译错误。

```go
str := "111"
str = str + "222"
```

## 使用缓冲区拼接字符串

如果需要在循环中拼接字符串，则使用空的字节缓冲区来拼接的效率更高。

```go
// 创建一个空的字节缓冲区
var buf bytes.Buffer

for i := 0; i < 100; i++ {
    buf.WriteString("a")
}
str := buf.String()
```

## 转换大小写

```go
str := "abc"
str = strings.ToUpper(str)
str = strings.ToLower(str)
```

## 查找子串

```go
str := "abcdef"
// 如果没有找到，就返回-1
i := strings.Index(str, "c")
```

## 删除空格

删除开头和末尾的空白

```go
str := " a b c "
// 输出:a b c
str = strings.TrimSpace(str)
```
