# JSON 转结构体

```go
package main

import (
	"encoding/json"
	"fmt"
)

type Student struct {
	Name string `json:"name"` // 需要手动转成驼峰
	Age  int    `json:"age"`
}

func main() {
	jsonString := `{"name":"John","age":18}`
	jsonBytes := []byte(jsonString)
	var s Student
	err := json.Unmarshal(jsonBytes, &s)
	if err != nil {
		return
	}
	fmt.Println(s.Name, s.Age)
}
```
