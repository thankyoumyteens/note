# 常量

定义常量的 2 种方式:

- 有类型常量: `const 常量名 常量类型 = 常量值`
  ```go
  const name string = "zhangsan"
  ```
- 无类型常量: `const 常量名 = 常量值`
  ```go
  const age = 10
  ```

```go
const a int = 1
const b = true
fmt.Println(a, b)
```

## 常量块

把同一类功能用到的常量定义在一起, 增强可读性:

```go
const (
    name = "zhangsan"
    age  = 10
)
```
