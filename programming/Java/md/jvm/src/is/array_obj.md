# 数组操作指令

普通对象和数组使用了不同的字节码指令。

## 创建数组

| 操作码         | 操作数                           | 操作数栈-执行前         | 操作数栈-执行后 | 操作                                                 |
| -------------- | -------------------------------- | ----------------------- | --------------- | ---------------------------------------------------- |
| newarray       | atype                            | count                   | arrayref        | 创建一个指定的原始类型(如 int, float, char 等)的数组 |
| anewarray      | indexbyte1,indexbyte2            | count                   | arrayref        | 创建一个引用型(如类, 接口, 数组)的数组               |
| multianewarray | indexbyte1,indexbyte2,dimensions | count1, \[count2, ...\] | arrayref        | 创建指定类型和指定维度的多维数组                     |

说明:

- newarray: count 为 int 类型的数据, 指令执行时它将从操作数栈中出栈, 它代表了要创建多大的数组。atype 为要创建数组的元素类型。一个以 atype 为组件类型、以 count 值为长度的数组将会被分配在堆中, 并且一个代表该数组的 reference 类型数据 arrayref 压入到操作数栈中。这个新数组的所有元素将会被分配为相应类型的初始值。atype 可选的值:
  - BOOLEAN: atype=4
  - CHAR: atype=5
  - FLOAT: atype=6
  - DOUBLE: atype=7
  - BYTE: atype=8
  - SHORT: atype=9
  - INT: atype=10
  - LONG: atype=11
- anewarray: count 应为 int 类型的数据, 指令执行时它将从操作数栈中出栈, 它代表了要创建多大的数组。indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个类、接口或者数组类型的符号引用, 这个类、接口或者数组类型应当是已被解析的。一个以此类型为组件类型、以 count 值为长度的数组将会被分配在堆中, 并且一个代表该数组的 reference 类型数据 arrayref 压入到操作数栈中。这个新数组的所有元素值都被初始化为 null, 也即是 reference 类型的默认值
- multianewarray: dimensions 操作数是一个无符号 byte 类型数据, 它必须大于或等于 1, 代表创建数组的维度。操作数栈中必须包含 dimensions 个数值, 操作数栈中的每一个值代表每个维度中需要创建的元素数量。这些值必须为非负数 int 类型数据。count1 描述第一个维度的长度, count2 描述第二个维度的长度, 依此类推。指令执行时, 所有 count 都将从操作数栈中出栈, 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个类、接口或者数组类型的符号引用, 这个类、接口或者数组类型应当是已被解析的。指令执行产生的结果将会是一个维度不小于 dimensions 的数组。一个新的多维数组将会被分配在堆中, 如果任何一个 count 值为 0, 那就不会分配维度。数组第一维的元素被初始化为第二维的子数组, 后面每一维都依此类推。数组的最后一个维度的元素将会被分配为数组元素类型的初始值。并且一个代表该数组的 reference 类型数据 arrayref 压入到操作数栈中

## 把一个数组元素加载到操作数栈

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                         |
| ------ | ------ | --------------- | --------------- | -------------------------------------------- |
| iaload | -      | arrayref,index  | value           | 将 int 型数组指定索引的值推送至栈顶          |
| laload | -      | arrayref,index  | value           | 将 long 型数组指定索引的值推送至栈顶         |
| faload | -      | arrayref,index  | value           | 将 float 型数组指定索引的值推送至栈顶        |
| daload | -      | arrayref,index  | value           | 将 double 型数组指定索引的值推送至栈顶       |
| baload | -      | arrayref,index  | value           | 将 boolean/byte 型数组指定索引的值推送至栈顶 |
| caload | -      | arrayref,index  | value           | 将 char 型数组指定索引的值推送至栈顶         |
| saload | -      | arrayref,index  | value           | 将 short 型数组指定索引的值推送至栈顶        |
| aaload | -      | arrayref,index  | value           | 将引用类型数组指定索引的值推送至栈顶         |

说明:

- iaload: arrayref 必须是一个 reference 类型的数据, 它指向一个组件类型为 int 的数组, index 必须为 int 类型。指令执行后, arrayref 和 index 同时从操作数栈出栈, index 作为索引定位到数组中的 int 类型值将压入到操作数栈中

## 给数组元素赋值

| 操作码  | 操作数 | 操作数栈-执行前      | 操作数栈-执行后 | 操作                                                    |
| ------- | ------ | -------------------- | --------------- | ------------------------------------------------------- |
| iastore | -      | arrayref,index,value | -               | 将栈顶 int 型数值存入指定数组的指定索引位置             |
| lastore | -      | arrayref,index,value | -               | 将栈顶 long 型数值存入指定数组的指定索引位置            |
| fastore | -      | arrayref,index,value | -               | 将栈顶 float 型数值存入指定数组的指定索引位置           |
| dastore | -      | arrayref,index,value | -               | 将栈顶 double 型数值存入指定数组的指定索引位置          |
| bastore | -      | arrayref,index,value | -               | 将栈顶 boolean 或 byte 型数值存入指定数组的指定索引位置 |
| castore | -      | arrayref,index,value | -               | 将栈顶 char 型数值存入指定数组的指定索引位置            |
| sastore | -      | arrayref,index,value | -               | 将栈顶 short 型数值存入指定数组的指定索引位置           |
| aastore | -      | arrayref,index,value | -               | 将栈顶引用类型值存入指定数组的指定索引位置              |

说明:

- iastore: arrayref 必须是一个 reference 类型的数据, 它指向一个组件类型为 int 的数组, index 和 value 都必须为 int 类型。指令执行后, arrayref、index 和 value 同时从操作数栈出栈, 然后 value 存储到 index 作为索引定位到的数组元素中

## 获取数组长度

| 操作码      | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                       |
| ----------- | ------ | --------------- | --------------- | -------------------------- |
| arraylength | -      | arrayref        | length          | 获取数组的长度值并压入栈顶 |

说明:

- arraylength: arrayref 必须是指向数组的 reference 类型的数据, 指令执行时, arrayref 从操作数栈中出栈, 数组的长度 length 将被计算出来并作为一个 int 类型数据压入到操作数栈中
