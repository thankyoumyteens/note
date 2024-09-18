# 解析命令行参数

Go 语言提供了 flag 包用来解析命令行参数。

## flag.数据类型

```go
参数指针名 := flag.数据类型(参数名, 默认值, 帮助文本)
```

示例

```go
package main

import (
	"flag"
	"fmt"
)

func main() {
	cp := flag.String("cp", "", "classpath")
	flag.Parse()

	if *cp == "" {
		fmt.Println("未指定classpath")
	} else {
		fmt.Println("classpath:", *cp)
	}
}
// 运行: ./hello
// 输出: 未指定classpath

// 运行: ./hello -cp aaa
// 输出: classpath: aaa
```

缺点: 需要频繁通过 `*` 来获取指针指向的数据。

## flag.数据类型 + Var

```go
flag.数据类型(参数变量地址, 参数名, 默认值, 帮助文本)
```

示例

```go
package main

import (
	"flag"
	"fmt"
)

func main() {
	var cp string
	flag.StringVar(&cp, "cp", "", "classpath")
	flag.Parse()

	if cp == "" {
		fmt.Println("未指定classpath")
	} else {
		fmt.Println("classpath:", cp)
	}
}
// 运行: ./hello
// 输出: 未指定classpath

// 运行: ./hello -cp aaa
// 输出: classpath: aaa
```

flag 包会自动创建显示帮助文本的命令:

```sh
./hello -h
./hello --h
./hello -help
./hello --hhelp
```

## Usage

每当在分析标志的过程中发生错误时，都将调用 Usage 函数:

```go
package main

import (
	"flag"
	"fmt"
	"os"
)

func printUsage() {
	fmt.Printf("Usage: %s -cp classpath\n", os.Args[0])
}
func main() {
	flag.Usage = printUsage
	flag.Parse()
}
```
