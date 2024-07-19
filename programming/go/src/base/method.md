# 方法

用来实现和 java 类的实例方法类似的功能。

```go
package main

import "fmt"

type Test struct {
    name string
}

// 为Test添加方法
func (t Test) getName() string {
    // t相当于this
    return t.name
}

// 为Test添加方法
func (t *Test) setName(name string) {
    // t相当于this
    t.name = name
}

func main() {
    var t Test
    t.setName("kevin")
    fmt.Println(t.getName())
}
```
