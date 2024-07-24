# error

创建 error

```go
package main

import (
    "errors"
    "fmt"
)

func main() {
    error1 := errors.New("error1")
    fmt.Println(error1)
    error2 := fmt.Errorf("error%d", 2)
    fmt.Println(error2)
}
```
