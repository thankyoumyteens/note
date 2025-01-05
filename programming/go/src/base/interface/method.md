# 方法

方法类似于函数, 但有一点不同: 在关键字 func 后面添加了一个接收者。接下来是方法名、参数以及返回类型。除了包含接收者的参数部分外, 方法与函数完全相同。

```go
type Student struct {
	name string
	age  int
}

func (s *Student) getAge() int {
	return s.age
}

func main() {
	s1 := Student{
		name: "Naveen",
		age:  10,
	}
	s2 := Student{
		name: "John",
		age:  20,
	}
	fmt.Println(s1.getAge())
	fmt.Println(s2.getAge())
}
```

接收者可以是指针, 也可以是值。将指针作为接收者的方法能够修改原始结构体的字段, 这是因为它使用的是指向原始结构体内存单元的指针, 因此操作的不是原始结构体的副本。
