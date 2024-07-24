# 自定义 error

```go
package main

import (
    "fmt"
)

type ServiceError struct {
    Code    int
    Message string
}

func (e *ServiceError) Error() string {
    return "Service Error"
}

func main() {
    error1 := ServiceError{
        Code:    1,
        Message: "1",
    }
    fmt.Println(error1)
}
```
