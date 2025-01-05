# Goroutine 的使用

Goroutine 使用起来非常简单, 只需在要让 Goroutine 执行的函数或方法前加上关键字 go 即可。

```go
package main

import (
	"fmt"
	"time"
)

func wait() {
	time.Sleep(5 * time.Second)
	fmt.Println("继续执行")
}

func main() {
	fmt.Println("123")
    // 使用Goroutine, wait函数就不会阻塞主线程
    // 而是立即返回
	go wait()
	fmt.Println("321")
	// 等待wait执行完毕
	time.Sleep(6 * time.Second)
}
```

与 Java 一样, Go 在幕后使用线程来管理并发, 但 Goroutine 让程序员无须直接管理线程。创建一个 Goroutine 只需占用几 KB 的内存, 因此即便创建数千个 Goroutine 也不会耗尽内存。另外, 创建和销毁 Goroutine 的效率也非常高。严格地说, Goroutine 并不是线程, 但可将其视为线程, 因为它们能够以非阻塞方式执行代码。
