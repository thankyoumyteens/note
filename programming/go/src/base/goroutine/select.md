# select 语句

假设有多个 Goroutine, 而程序将根据最先返回的 Goroutine 执行相应的操作, 此时可使用 select 语句。select 语句类似于 switch 语句, 它为通道创建一系列接收者, 并执行最先收到消息的接收者。

```go
package main

import (
	"fmt"
	"time"
)

func send(c chan string, duration time.Duration) {
	time.Sleep(duration * time.Second)
	c <- "继续执行"
}

func main() {
	channel1 := make(chan string)
	channel2 := make(chan string)

	go send(channel1, 2)
	go send(channel2, 1)

	select {
	case msg1 := <-channel1:
		fmt.Println("1 received", msg1)
	case msg2 := <-channel2:
		fmt.Println("2 received", msg2)
	}
}
```

如果从通道 channel1 那里收到了消息, 将执行第一条 case 语句。如果从通道 channel2 那里收到了消息, 将执行第二条 case 语句。具体执行哪条 case 语句, 取决于消息到达的时间, 哪条消息最先到达决定了将执行哪条 case 语句。通常, 接下来收到的其他消息将被丢弃。收到一条消息后, select 语句将不再阻塞。可以搭配 for 循环来实现一直接收消息。

可以使用超时时间, 让 select 语句在指定时间后不再阻塞, 接着往下执行。

```go
select {
case msg1 := <-channel1:
	fmt.Println("1 received", msg1)
case msg2 := <-channel2:
	fmt.Println("2 received", msg2)
// 500毫秒后, 如果channel1和channel2都没有收到消息
// 将输出timeout并继续往下执行
case <-time.After(500 * time.Millisecond):
	fmt.Println("timeout")
}
```

## 退出通道

通过在 select 语句中添加一个退出通道, 可向退出通道发送消息来结束该语句, 从而停止继续监听。

```go
messages := make(chan string)
stop := make(chan bool)

for {
    select {
    case <-stop:
        return
    case msg := <-messages:
        fmt.Println(msg)
    }
}
```
