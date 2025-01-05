# 切片

切片是底层数组中的一个连续片段, 切片比数组更灵活, 既可以在切片中添加和删除元素, 还可以复制切片中的元素。可将切片视为轻量级的数组包装器, 它既保留了数组的完整性, 又比数组使用起来更容易。

声明切片:

```go
// 声明空切片
var 切片名 = make([]数据类型, 初始容量)
// 简短变量声明, 并指定初始值
切片名 := []数据类型{初始值1, 初始值2, ...}
```

创建切片后, 可像给数组赋值一样给切片赋值。

```go
package main

import "fmt"

func main() {
	var s = make([]int, 5)
	s[0] = 1
	fmt.Println(s[0])
}
```

不同于数组的是, 在切片中可以添加和删除元素。

## 在切片中添加元素

使用 append 函数, 能够增大切片的长度。append 是一个可变参数的函数, 使用函数 append 可以一次在切片末尾添加多个值。

```go
package main

import "fmt"

func main() {
	var s = make([]int, 1)
	s = append(s, 2, 3)
	fmt.Println(s[2])
}
```

## 从切片中删除元素

要从切片中删除元素, 也可以使用 append 函数。

```go
package main

import "fmt"

func main() {
	var s = make([]int, 10)
	// 删除索引2处的元素
	s = append(s[:2], s[2+1:]...)
	fmt.Println(s)
}
```

## 复制切片中的元素

要复制切片的全部或部分元素, 可使用内置函数 copy。在复制切片中的元素前, 必须再声明一个类型与该切片相同的切片。函数 copy 在新切片中创建元素的副本, 因此修改一个切片中的元素不会影响另一个切片。

```go
package main

import "fmt"

func main() {
	src := []int{1, 2, 3, 4, 5}
	var target = make([]int, 5)
	copy(target, src)
	fmt.Println(target)
}
```

还可将单个元素或特定范围内的元素复制到新切片中:

```go
copy(target, src[1:3])
```
