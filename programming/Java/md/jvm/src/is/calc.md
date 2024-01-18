# 算术指令

算术指令用于对两个操作数栈上的值进行某种特定运算，并把结果重新存入到操作栈顶。不存在直接支持 byte、short、char 和 boolean 类型的算术指令，对于上述几种数据的运算，应使用操作 int 类型的指令代替。

## 加法

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                         |
| ------ | ------ | --------------- | --------------- | -------------------------------------------- |
| iadd   | -      | value1,value2   | result          | 将栈顶两个 int 型数值相加并将结果压入栈顶    |
| ladd   | -      | value1,value2   | result          | 将栈顶两个 long 型数值相加并将结果压入栈顶   |
| fadd   | -      | value1,value2   | result          | 将栈顶两个 float 型数值相加并将结果压入栈顶  |
| dadd   | -      | value1,value2   | result          | 将栈顶两个 double 型数值相加并将结果压入栈顶 |

说明:

- iadd: value1 和 value2 都必须为 int 类型数据，指令执行时，value1 和 value2 从操作数栈中出栈，将这两个数值相加得到 int 类型数据 result，最后 result 被压入到操作数栈中

## 减法

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                         |
| ------ | ------ | --------------- | --------------- | -------------------------------------------- |
| isub   | -      | value1,value2   | result          | 将栈顶两个 int 型数值相减并将结果压入栈顶    |
| lsub   | -      | value1,value2   | result          | 将栈顶两个 long 型数值相减并将结果压入栈顶   |
| fsub   | -      | value1,value2   | result          | 将栈顶两个 float 型数值相减并将结果压入栈顶  |
| dsub   | -      | value1,value2   | result          | 将栈顶两个 double 型数值相减并将结果压入栈顶 |

说明:

- isub: value1 和 value2 都必须为 int 类型数据，指令执行时，value1 和 value2 从操作数栈中出栈，将这两个数值相减，结果转换为 int 类型值 result，最后 result 被压入到操作数栈中

## 乘法

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                         |
| ------ | ------ | --------------- | --------------- | -------------------------------------------- |
| imul   | -      | value1,value2   | result          | 将栈顶两个 int 型数值相乘并将结果压入栈顶    |
| lmul   | -      | value1,value2   | result          | 将栈顶两个 long 型数值相乘并将结果压入栈顶   |
| fmul   | -      | value1,value2   | result          | 将栈顶两个 float 型数值相乘并将结果压入栈顶  |
| dmul   | -      | value1,value2   | result          | 将栈顶两个 double 型数值相乘并将结果压入栈顶 |

说明:

- imul: value1 和 value2 都必须为 int 类型数据，指令执行时，value1 和 value2 从操作数栈中出栈，接着将这两个数值相乘，结果压入到操作数栈中

## 除法

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                         |
| ------ | ------ | --------------- | --------------- | -------------------------------------------- |
| idiv   | -      | value1,value2   | result          | 将栈顶两个 int 型数值相除并将结果压入栈顶    |
| ldiv   | -      | value1,value2   | result          | 将栈顶两个 long 型数值相除并将结果压入栈顶   |
| fdiv   | -      | value1,value2   | result          | 将栈顶两个 float 型数值相除并将结果压入栈顶  |
| ddiv   | -      | value1,value2   | result          | 将栈顶两个 double 型数值相除并将结果压入栈顶 |

说明:

- idiv: value1 和 value2 都必须为 int 类型数据，指令执行时，value1 和 value2 从操作数栈中出栈，并且将这两个数值相除，结果转换为 int 类型值 result，最后 result 被压入到操作数栈中

## 取余

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                               |
| ------ | ------ | --------------- | --------------- | -------------------------------------------------- |
| irem   | -      | value1,value2   | result          | 将栈顶两个 int 型数值作取模运算并将结果压入栈顶    |
| lrem   | -      | value1,value2   | result          | 将栈顶两个 long 型数值作取模运算并将结果压入栈顶   |
| frem   | -      | value1,value2   | result          | 将栈顶两个 float 型数值作取模运算并将结果压入栈顶  |
| drem   | -      | value1,value2   | result          | 将栈顶两个 double 型数值作取模运算并将结果压入栈顶 |

说明:

- irem: value1 和 value2 都必须为 int 类型数据，指令执行时，value1 和 value2 从操作数栈中出栈，根据 `value1-(value1÷value2)×value2` 计算出结果，然后把运算结果入栈回操作数栈中
