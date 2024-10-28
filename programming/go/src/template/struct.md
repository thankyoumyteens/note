# 访问结构体的字段

- `{{ . }}` 点表示传入的结构体
- `{{ .字段名 }}` 访问结构体的字段

```go
package main

import (
	"bytes"
	"fmt"
	"text/template"
)

type Person struct {
	Name string
	Age  int
}

// 模版内容
// 访问Name和Age字段
var templateContent = `
Name: {{ .Name }}
Age: {{ .Age }}
`

func main() {
	// 要渲染的数据
	data := Person{
		Name: "Tom",
		Age:  18,
	}

	t := template.New("name")
	// 解析模版
	parsedTemplate, _ := t.Parse(templateContent)
	buffer := new(bytes.Buffer)
	// 渲染模版
	_ = parsedTemplate.Execute(buffer, data)
	fmt.Println(buffer.String())
}
```
