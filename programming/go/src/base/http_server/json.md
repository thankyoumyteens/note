# 读写JSON

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Words struct {
	SourceTet     string `json:"sourceText"`
	Translation   string `json:"translation"`
	Pronunciation string `json:"pronunciation"`
}

type ResponseData struct {
	Status  int    `json:"status"`
	Message string `json:"message"`
}

func main() {
	http.HandleFunc("/demo", func(writer http.ResponseWriter, request *http.Request) {

		bytes, err := io.ReadAll(request.Body)
		if err != nil {
			return
		}

		words := Words{}
		err = json.Unmarshal(bytes, &words)
		if err != nil {
			return
		}

		fmt.Println(words)

        r := ResponseData{
            Status:  0,
            Message: "操作成功",
        }
        bytes, err := json.Marshal(r)
        if err != nil {
            return
        }
		writer.Header().Set("Content-Type", "application/json")
        writer.Write(bytes)
	})
	http.ListenAndServe(":8080", nil)
}
```
