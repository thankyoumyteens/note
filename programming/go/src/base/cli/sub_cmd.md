# 创建子命令

子命令: 比如 `git clone`, clone 就是 git 的子命令。

```go
package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	subCommand := flag.NewFlagSet("clone", flag.ExitOnError)
	switch os.Args[1] {
	case "clone":
		url := subCommand.String("u", "", "url")
		err := subCommand.Parse(os.Args[2:])
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Println(*url)
	default:
		return
	}
}
```
