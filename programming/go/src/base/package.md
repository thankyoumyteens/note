# 包

可导出函数: 首字母大写的函数。首字母小写的函数不能在包外使用。

## 导入包

```go
import "包名"
import 别名 "包名"
```

## init 函数

包被导入时自动执行的函数。

```go
func init() {
    // do something
}
```

## 构建成可执行文件

```go
go build xxx.go
```
