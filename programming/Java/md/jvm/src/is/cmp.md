# 比较指令

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                         |
| ------ | ------ | --------------- | --------------- | ---------------------------- |
| lcmp   | -      | value1,value2   | result          | 比较栈顶两 long 型数值大小   |
| fcmpl  | -      | value1,value2   | result          | 比较栈顶两 float 型数值大小  |
| fcmpg  | -      | value1,value2   | result          | 比较栈顶两 float 型数值大小  |
| dcmpl  | -      | value1,value2   | result          | 比较栈顶两 double 型数值大小 |
| dcmpg  | -      | value1,value2   | result          | 比较栈顶两 double 型数值大小 |

说明:

- lcmp: value1 和 value2 都必须为 long 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 使用一个 int 数值作为比较结果: 如果 value1 大于 value2, 结果为 1。如果 value1 等于 value2, 结果为 0。如果 value1 小于 value2, 结果为-1。最后比较结果被压入到操作数栈中
- fcmp: value1 和 value2 都必须为 float 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 并且经过数值集合转换后得到值 value1’ 和 value2’, 接着对这 2 个值进行浮点比较操作:  如果 value1’大于 value2’ 的话, int 值 1 将压入到操作数栈中。如果 value1’ 与 value2’ 相等的话, int 值 0 将压入到操作数栈中。如果 value1’ 小于 value2’ 相等的话, int 值-1 将压入到操作数栈中。如果 value1’ 和 value2’ 之中最少有一个为 NaN, 那 fcmpg 指令将 int 值 1 压入到操作数栈中, 而 fcmpl 指令则把 int 值-1 压入到操作数栈中
