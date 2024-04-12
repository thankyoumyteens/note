# 对象操作指令

普通对象和数组使用了不同的字节码指令。

## 创建对象

| 操作码 | 操作数                | 操作数栈-执行前 | 操作数栈-执行后 | 操作         |
| ------ | --------------------- | --------------- | --------------- | ------------ |
| new    | indexbyte1,indexbyte2 | -               | objectref       | 创建一个对象 |

说明:

- new: 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个类或接口的符号引用, 这个类或接口类型应当是已被解析并且最终解析结果为某个具体的类型。一个以此为类型的对象将会被分配在堆中, 并且它所有的实例变量都会进行初始化为相应类型的初始值。一个代表该对象实例的 reference 类型数据 objectref 将压入到操作数栈中。对于一个已成功解析但是未初始化的类型, 在这时将会进行初始化

注意: new 指令执行后并没有完成一个对象实例创建的全部过程, 创建一个对象通常是 new、dup、invokespecial 三条指令一起出现。

## 操作字段

| 操作码    | 操作数                | 操作数栈-执行前 | 操作数栈-执行后 | 操作                   |
| --------- | --------------------- | --------------- | --------------- | ---------------------- |
| getstatic | indexbyte1,indexbyte2 | -               | value           | 获取指定类的静态字段   |
| putstatic | indexbyte1,indexbyte2 | value           | -               | 为指定类的静态字段赋值 |
| getfield  | indexbyte1,indexbyte2 | objectref       | value           | 获取指定类的字段       |
| putfield  | indexbyte1,indexbyte2 | objectref,value | -               | 为指定类的字段赋值     |

说明:

- getstatic: 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个字段的符号引用, 它包含了字段的名称和描述符, 以及包含该字段的类或接口的符号引用。这个字段的符号引用是已被解析过的。在字段被成功解析之后, 如果字段所在的类或者接口没有被初始化过, 那指令执行时将会触发其初始化过程。参数所指定的类或接口的该字段的值将会被取出, 并推入到操作数栈顶
- putstatic: 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个字段的符号引用, 它包含了字段的名称和描述符, 以及包含该字段的类或接口的符号引用。这个字段的符号引用是已被解析过的。在字段被成功解析之后, 如果字段所在的类或者接口没有被初始化过, 那指令执行时将会触发其初始化过程。被 putstatic 指令存储到字段中的 value 值的类型必须与字段的描述符相匹配。如果字段描述符的类型是 boolean、byte、char、short 或者 int, 那么 value 必须为 int 类型。如果字段描述符的类型是 float、long 或者 double, 那 value 的类型必须相应为 float、long 或者 double。如果字段描述符的类型是 reference 类型, 那 value 必须为一个可与之匹配的类型。如果字段被声明为 final 的, 那就只能在当前类的`<clinit>`方法中设置当前类的 final 字段。指令执行时, value 从操作数栈中出栈, 为类的指定字段赋值
- getfield: objectref 必须是一个 reference 类型的数据, 在指令执行时, objectref 将从操作数栈中出栈。无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个字段的符号引用, 它包含了字段的名称和描述符, 以及包含该字段的类的符号引用。这个字段的符号引用是已被解析过的。指令执行后, 被 objectref 所引用的对象中该字段的值将会被取出, 并推入到操作数栈顶。objectref 所引用的对象不能是数组类型, 如果取值的字段是 protected 的, 并且这个字段是当前类的父类成员, 并且这个字段没有在同一个运行时包中定义过, 那 objectref 所指向的对象的类型必须为当前类或者当前类的子类
- putfield: 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个字段的符号引用, 它包含了字段的名称和描述符, 以及包含该字段的类的符号引用。objectref 所引用的对象不能是数组类型, 如果取值的字段是 protected 的, 并且这个字段是当前类的父类成员, 并且这个字段没有在同一个运行时包中定义过, 那 objectref 所指向的对象的类型必须为当前类或者当前类的子类。这个字段的符号引用是已被解析过的。被 putfield 指令存储到字段中的 value 值的类型必须与字段的描述符相匹配。如果字段描述符的类型是 boolean、byte、char、short 或者 int, 那么 value 必须为 int 类型。如果字段描述符的类型是 float、long 或者 double, 那 value 的类型必须相应为 float、long 或者 double。如果字段描述符的类型是 reference 类型, 那 value 必须为一个可与之匹配的类型。如果字段被声明为 final 的, 那就只能在当前类的`<init>`方法中设置当前类的 final 字段。指令执行时, value 和 objectref 从操作数栈中出栈, objectref 必须为 reference 类型数据, value 为 objectref 的指定字段的值
