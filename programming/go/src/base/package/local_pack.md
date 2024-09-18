# 使用本地包

目录结构(其它包不能和 main 包在同一级)

```
.
├── go.mod
├── hello.go
└── test
    └── test.go
```

test 包的内容

```go
package test

func Test() string {
	return "Hello World!"
}
```

使用 test 包

```go
package main

import (
	"mygodemo/test"
	"fmt"
)

func main() {
	fmt.Println(test.Test())
}
```
