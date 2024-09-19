# 基本使用

```go
package main

import (
	"io"
	"net/http"
	"strings"
)

func main() {
	// 发送GET请求
	resp, err := http.Get("http://localhost:8080/get?name=test")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	bytes, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	println(string(bytes))

	// 发送POST请求
	postData := strings.NewReader(`{"name":"test"}`)
	resp, err = http.Post("http://localhost:8080", "application/json", postData)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	bytes, err = io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	println(string(bytes))
}
```
