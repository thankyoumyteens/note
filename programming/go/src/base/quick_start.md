# 运行 go 程序

1. 创建 hello.go 文件

```sh
mkdir hello/
cd hello/
go mod init hello
vim hello.go
```

2. 内容

```go
package main

import (
	"fmt"
)

func main() {
	fmt.Println("Hello, World!")
}
```

3. 运行

```sh
go run hello.go
```
