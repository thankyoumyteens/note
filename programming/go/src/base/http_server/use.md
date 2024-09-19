# 基本使用

```go
package main

import "net/http"

func main() {
	// http://localhost:8080/
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Hello, World!"}`))
	})
	// http://localhost:8080/getWithParams
	// 获取 URL 参数
	http.HandleFunc("/getWithParams", func(w http.ResponseWriter, r *http.Request) {
		name := r.URL.Query().Get("name")
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Hello, ` + name + `!"}`))
	})
	// http://localhost:8080/postFormWithParams
	// 获取表单参数
	http.HandleFunc("/postFormWithParams", func(w http.ResponseWriter, r *http.Request) {
		name := r.FormValue("name")
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Hello, ` + name + `!"}`))
	})
	http.ListenAndServe(":8080", nil)
}
```
