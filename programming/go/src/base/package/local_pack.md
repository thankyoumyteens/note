# 使用本地包

1. 目录结构(其它包不能和 main 包在同一级)

```
└── project1
    ├── go.mod
    └── hello.go
    └── dir1
        └── test.go
```

2. test.go

```go
package test

func Test() string {
	return "Hello World!"
}
```

3. hello.go

```go
package main

import (
	"project1/dir1"
	"fmt"
)

func main() {
	fmt.Println(test.Test())
}
```

4. 运行

```sh
go run hello.go
```

## 使用其它项目的本地包

1. 目录结构

```
├── project2
│   ├── go.mod
│   └── test.go
└── project1
    ├── go.mod
    └── hello.go
```

2. test.go

```go
package test

func Test() string {
	return "Hello World!"
}
```

3. project1/go.mod 中按相对路径来寻找 project2

```go
module hello

go 1.23.1

// => 左边的名字随便取
// => 右边使用绝对路径和相对路径都行
replace project2 => ../project2

// 版本号随便写, 但是必须是 vX.X.X 的形式, 至少要两个点
require project2 v1.0.0
```

4. hello.go

```go
package main

import (
	"project2"
	"fmt"
)

func main() {
	fmt.Println(test.Test())
}
```

5. 在 project1 下执行

```sh
go mod tidy
```

6. 运行

```sh
go run hello.go
```
