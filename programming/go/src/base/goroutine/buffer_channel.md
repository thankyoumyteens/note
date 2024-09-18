# 缓冲通道

通常，通道收到消息后就可将其发送给接收者，但有时候可能没有接收者。在这种情况下，可使用缓冲通道。缓冲通道可将数据存储在通道中，等接收者准备就绪再交给它。

创建缓冲通道:

```go
通道名 := make(chan 通道中存储的数据类型, 缓冲区长度)
```

缓冲通道最多只能存储指定数量的消息，如果向它发送更多的消息将导致错误。

```go
package main

import (
	"fmt"
)

func showMsg(c chan string) {
	for msg := range c {
		fmt.Println(msg)
	}
}

func main() {
	// 创建一个存储字符串数据的缓冲通道
	c := make(chan string, 2)

	c <- "Hello"
	c <- "World"
	// 关闭通道，禁止再向通道发送消息
	// 但是可以继续从通道接收消息
	// 不加这个会报错：fatal error: all goroutines are asleep - deadlock!
	close(c)
	showMsg(c)
}
```
