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

replace project2 => ../project2
```

4. 在 project1 下执行

```sh
go mod tidy
```

5. hello.go

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

6. 运行

```sh
go run hello.go
```
