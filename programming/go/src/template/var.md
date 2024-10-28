# 声明变量

- `{{ $变量名 := 值 }}` 声明变量
- `{{ $变量名 = 值 }}` 给变量重新赋值
- `{{ $var }}` 访问变量

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
{{ $tmp := .Name }}
Name: {{ $tmp }}
{{ $tmp = .Age }}
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
