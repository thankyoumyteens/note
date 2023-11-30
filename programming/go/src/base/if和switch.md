# if 和 switch

## if

```go
package main

import "fmt"

func main() {
	x := 2
	y := 1
	z := 2
	if x < y {
		fmt.Printf("x")
	} else if x > z {
		fmt.Printf("z")
	} else {
		fmt.Printf("y")
	}
}
// 输出:
// y
```

## switch

```go
package main

import "fmt"

func main() {
	x := 2
	switch x {
	case 1:
		fmt.Printf("1")
	case 2:
		fmt.Printf("2")
	case 3:
		fmt.Printf("3")
	}
}
// 输出:
// 2
```

## fallthrough

在 Go 中 case 是一个独立的代码块，执行完毕后不会紧接着执行下一个 case。

使用 fallthrough 会强制执行后面的 case 语句。

```go
package main

import "fmt"

func main() {
	x := 2
	switch x {
	case 1:
		fmt.Printf("1")
		fallthrough
	case 2:
		fmt.Printf("2")
		fallthrough
	case 3:
		fmt.Printf("3")
	}
}
// 输出:
// 23
```
