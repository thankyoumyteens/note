# for

```go
package main

import "fmt"

func main() {
    // fori
	for a := 0; a < 3; a++ {
		fmt.Printf("a = %d\n", a)
	}
    // while
	b := 0
	for b < 3 {
		b++
		fmt.Printf("b = %d\n", b)
	}
    // while(true)
	for {
		fmt.Printf("1")
	}
}
// 输出:
// a = 0
// a = 1
// a = 2
// b = 1
// b = 2
// b = 3
// 11111111111...
```
