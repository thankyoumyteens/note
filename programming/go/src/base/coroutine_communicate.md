# 协程通信

使用 channel 实现。

## 无缓冲的 channel 同步通信

```go
package main

import (
    "fmt"
    "strconv"
    "sync"
    "time"
)

// chan<- string 是channel的类型, 表示一个string队列
func producer(ch chan<- string) {
    for i := 0; i < 10; i++ {
        // 向chanel中写数据,
        // 如果此时channel中缓冲区满了则会阻塞,
        // 等待channel中的数据被取出后才能继续执行
        val := "value" + strconv.Itoa(i)
        ch <- val
        fmt.Println("produced: " + val)
    }
    // 通知消费者停止接收
    // 不加这个的话, 消费者会一直阻塞, 导致程序报错
    close(ch)
}

func consumer(ch <-chan string, wg *sync.WaitGroup) {
    defer wg.Done()
    // 从channel中取数据, 没有数据的话会阻塞等待
    for data := range ch {
        fmt.Println("consume: " + data)
        time.Sleep(1 * time.Second)
    }
}

func main() {
    // 创建无缓冲的 channel
    // 写入一条数据后缓冲区就满了
    ch := make(chan string)
    wg := sync.WaitGroup{}
    wg.Add(1)
    // 启动协程
    go producer(ch)
    // 启动协程
    go consumer(ch, &wg)
    wg.Wait()
}
```

## 有缓冲的 channel 异步通信

和无缓冲的 channel 的唯一区别就是指定了缓冲区的大小。

```go
// 创建缓冲区大小为10的 channel
// 写入10条数据后缓冲区就满了
ch := make(chan string, 10)
```

## select

select 可以监听多个 channel 的消息。

```go
package main

import (
    "fmt"
    "strconv"
    "sync"
    "time"
)

// chan<- string 是channel的类型, 表示一个string队列
func producer(ch chan<- string) {
    for i := 0; i < 10; i++ {
        // 向chanel中写数据,
        // 如果此时channel中缓冲区满了则会阻塞,
        // 等待channel中的数据被取出后才能继续执行
        val := "value" + strconv.Itoa(i)
        ch <- val
        fmt.Println("produced: " + val)
    }

    // 没有数据在select的default中处理, 不需要close了
}

func consumer(ch <-chan string, wg *sync.WaitGroup) {
    defer wg.Done()
    for {
        select {
        case data := <-ch:
            // 每个case监听一个channel
            fmt.Println("consume: " + data)
        default:
            // 没有数据
            fmt.Println("empty channel")
            time.Sleep(1 * time.Second)
        }
    }
}

func main() {
    // 创建无缓冲的 channel
    // 写入一条数据后缓冲区就满了
    ch := make(chan string)
    wg := sync.WaitGroup{}
    wg.Add(1)
    // 启动协程
    go producer(ch)
    // 启动协程
    go consumer(ch, &wg)
    wg.Wait()
}
```
