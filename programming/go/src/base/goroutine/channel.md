# 通道

通道让数据能够进入和离开 Goroutine, 可方便 Goroutine 之间进行通信。​Go 语言使用通道在 Goroutine 之间收发消息, 避免了使用共享内存。

创建通道:

```go
通道名 := make(chan 通道中存储的数据类型)
```

向通道发送消息(以字符串为例)

```go
// <- 表示将右边的字符串发送给左边的通道
c <- "hello"
```

从通道接收消息(以字符串为例)

```go
msg := <-c
```

使用通道进行通信:

```go
package main

import (
	"fmt"
	"time"
)

// 将通道当作参数
func wait(c chan string) {
	time.Sleep(5 * time.Second)
	c <- "继续执行"
}

func main() {
	// 创建一个存储字符串数据的通道
	c := make(chan string)

	go wait(c)
	// 接收来自通道c的消息, 这将阻塞进程直到收到消息为止
	msg := <-c
	fmt.Println(msg)
}
```
