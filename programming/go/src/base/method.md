# 方法

用来实现和 java 类的实例方法类似的功能。

```go
type Test struct{}

func (t Test) methodA() int {
    // t相当于this
    return 1
}

func (t *Test) methodB(a, b int) int {
    // t相当于this
    return 1
}
```

使用方法

```go
t1 := Test{}
r := t1.methodA()
```
