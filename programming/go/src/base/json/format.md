# 结构体转 JSON

```go
package main

import "encoding/json"

type Student struct {
	Name string `json:"name"` // 需要手动转成驼峰
	Age  int    `json:"age"`
}

func main() {
	s := Student{
		Name: "John",
		Age:  18,
	}
	jsonBytes, err := json.Marshal(s)
	if err != nil {
		return
	}
	jsonString := string(jsonBytes)
	println(jsonString)
}
```
