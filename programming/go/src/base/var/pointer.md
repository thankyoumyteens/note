# 指针

要获取变量在计算机内存中的地址, 可在变量名前加上 `&` 字符。

```go
package main

import "fmt"

func main() {
	a := 100
	// 输出: 0x1400005e730
	fmt.Println(&a)
}
```

将变量传递给函数时, 会分配新内存并将变量的值复制到其中, 这将占用更多的内存。

指针指向变量所在的内存单元。要声明指针, 可在变量名前加上 `*` 字符。

```go
package main

import "fmt"

func printPointer(p *int) {
	// 打印a的地址
	fmt.Println(p)
	// 打印a的值
	fmt.Println(*p)
}

func main() {
	a := 100
	printPointer(&a)
}
```
