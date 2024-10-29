# 遍历

## 遍历 map

- 格式: `{{ range $k, $v := 字典 }} 键为{{ $k }} 值为{{ $v }} {{ end }}`

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
{{ range $k, $v := . }}
姓名: {{ $k }} 年龄: {{ $v.Age }}
{{ end }}
`

func main() {
	// 要渲染的数据
	mapData := map[string]Person{
		"Tom": {Name: "Tom", Age: 18},
	}

	t := template.New("name")
	// 解析模版
	parsedTemplate, _ := t.Parse(templateContent)
	buffer := new(bytes.Buffer)
	// 渲染模版
	_ = parsedTemplate.Execute(buffer, mapData)
	fmt.Println(buffer.String())
}
```

在 range 和 end 内部如果要使用外部的变量，比如 `.Var2`，需要在点前加上 `$` 符号: `$.Var2`。

## 遍历切片

- 格式: `{{ range $i, $v := 切片 }} 索引为{{ $i }} 值为{{ $v }} {{ end }}`

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
{{ range $i, $v := . }}
索引: {{ $i }} 姓名: {{ $v.Name }}
{{ end }}
`

func main() {
	// 要渲染的数据
	listData := []Person{
		{Name: "Tom", Age: 18},
	}

	t := template.New("name")
	// 解析模版
	parsedTemplate, _ := t.Parse(templateContent)
	buffer := new(bytes.Buffer)
	// 渲染模版
	_ = parsedTemplate.Execute(buffer, listData)
	fmt.Println(buffer.String())
}
```
