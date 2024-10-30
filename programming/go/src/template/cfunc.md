# 自定义函数

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
{{ printPerson . }}
`

// 自定义函数
func printPerson(p Person) string {
	return fmt.Sprintf("Name: %s, Age: %d", p.Name, p.Age)
}

func main() {
	// 要渲染的数据
	data := Person{
		Name: "Tom",
		Age:  18,
	}

	// 在FuncMap中声明要使用的函数
	funcMap := template.FuncMap{
		"printPerson": printPerson,
	}

	t := template.New("name")
	// 注册FuncMap
	t.Funcs(funcMap)
	// 解析模版
	parsedTemplate, _ := t.Parse(templateContent)
	buffer := new(bytes.Buffer)
	// 渲染模版
	_ = parsedTemplate.Execute(buffer, data)
	fmt.Println(buffer.String())
}
```
