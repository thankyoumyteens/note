# 内置函数

- `eq 值1 值2` 如果值 1 = 值 2 则返回 true, 否则返回 false
- `ne 值1 值2` 如果值 1 ≠ 值 2 则返回 true, 否则返回 false
- `lt 值1 值2` 如果值 1 < 值 2 则返回 true, 否则返回 false
- `le 值1 值2` 如果值 1 ≤ 值 2 则返回 true, 否则返回 false
- `gt 值1 值2` 如果值 1 > 值 2 则返回 true, 否则返回 false
- `ge 值1 值2` 如果值 1 ≥ 值 2 则返回 true, 否则返回 false

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
{{ eq .Name "Tom" }}
{{ eq .Name "Jerry" }}
{{ eq .Age 10 }}
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
