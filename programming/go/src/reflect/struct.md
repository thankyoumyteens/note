# 遍历结构体

```go
package main

import (
	"fmt"
	"reflect"
)

type Demo struct {
	Name string `title:"姓名"`
	Age  int    `title:"年龄"`
}

func traversalStruct(obj interface{}) {
	// 获取结构体类型信息
	t := reflect.TypeOf(obj)
	// 用来获取obj中具体的值
	v := reflect.ValueOf(obj)
	// 获取结构体的字段数量
	num := t.NumField()
	// 遍历所有字段
	for i := 0; i < num; i++ {
		// 获取字段
		field := t.Field(i)
		// 获取字段名
		name := field.Name
		// 获取字段值
		value := v.Field(i).Interface()
		// 获取tag值
		tag := field.Tag.Get("title")

		fmt.Printf("字段名：%s, 字段值：%v, tag：%s\n", name, value, tag)
	}
}

func main() {
	demo := Demo{Name: "tom", Age: 18}
	traversalStruct(demo)
}
```
