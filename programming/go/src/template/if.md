# 分支

- `{{ if 条件 }} 输出1 {{ else if 条件 }} 输出2 {{ else }} 输出3 {{ end }}`

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
var templateContent = `
{{ if eq .Name "Tom" }}
Tom
{{ else if eq .Name "Jerry" }}
Jerry
{{ else }}
others
{{ end }}
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
