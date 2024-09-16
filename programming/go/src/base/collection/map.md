# 映射

映射可视为键-值对集合, 它映射在信息查找方面的效率非常高，因为可直接通过键来检索数据。

声明映射:

```go
// 声明空映射
var 映射名 = make(map[键的数据类型]值的数据类型)
```

变量名后面的方括号内为键，而等号右边是要赋给键的值。可使用这个键来获取相应的值。

```go
package main

import "fmt"

func main() {
	var dict = make(map[string]string)
	dict["name"] = "Gopher"
	dict["age"] = "10"
	fmt.Println(dict["name"])
}
```

## 从映射中删除元素

要从映射中删除元素，可使用内置函数 delete。

```go
package main

import "fmt"

func main() {
	var dict = make(map[string]string)
	dict["name"] = "Gopher"
	dict["age"] = "10"
	delete(dict, "age")
	fmt.Println(dict)
}
```
