# 接口

```go
package main

import "fmt"

// 接口
type Speak interface {
    say()
}

type male struct {
}
type female struct {
}

// 实现接口的方法
func (m male) say() {
    fmt.Println("Male")
}

// 实现接口的方法
func (f female) say() {
    fmt.Println("Female")
}

func main() {
    var speaker Speak
    speaker = male{}
    speaker.say()
    speaker = female{}
    speaker.say()
}
```

## 实现多个接口

```go
type Input interface {
    read() string
}

type Output interface {
    write(s string)
}

type worker struct {
    buffer string
}

func (w *worker) read() string {
    return w.buffer
}

func (w *worker) write(s string) {
    w.buffer = s
}
```
