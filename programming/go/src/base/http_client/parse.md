# 解析 JSON

```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type ResObj struct {
	Login  string `json:"login"`
	Id     int    `json:"id"`
	NodeId string `json:"node_id"`
}

func main() {
	var obj ResObj
	resp, err := http.Get("https://api.github.com/users/shapeshed")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	// 解析json
	decoder := json.NewDecoder(resp.Body)
	err = decoder.Decode(&obj)
	if err != nil {
		panic(err)
	}
	fmt.Println(obj)
}
```
