# 协程

go 使用协程实现并发。

## 创建协程

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    for i := 0; i < 10; i++ {
        // 创建协程
        go func(indexFromLoop int) {
            fmt.Println("i = ", indexFromLoop)
        }(i)
    }
    // 等待协程执行完
    time.Sleep(1 * time.Second)
}
```

## 等待协程执行完闭

使用 `sync.WaitGroup`, 类似于 java 中的 CountDownLatch:

1. Add: 设置计数
2. Done: 计数减一
3. Wait: 等待计数为 0 后继续执行

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var eg sync.WaitGroup

    eg.Add(10)

    for i := 0; i < 10; i++ {
        go func(indexFromLoop int) {
            // 使用defer避免异常导致eg.Done()无法执行
            defer func() {
                eg.Done()
            }()
            fmt.Println("i = ", indexFromLoop)
        }(i)
    }
    // 等待协程执行完
    eg.Wait()
}
```

## 互斥锁

使用 `sync.Mutex`:

1. Lock: 加锁
2. Unlock: 解锁

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    sharedMap := make(map[int]string)

    var (
        eg   sync.WaitGroup
        // 锁
        lock sync.Mutex
    )
    eg.Add(10)
    for i := 0; i < 10; i++ {
        go func(indexFromLoop int) {
            defer func() {
                // 解锁
                lock.Unlock()
                eg.Done()
            }()
            // 加锁
            lock.Lock()
            sharedMap[indexFromLoop] = "ok"
        }(i)
    }
    eg.Wait()
    fmt.Println(sharedMap)
}
```
