# 算术指令

算术指令用于对两个操作数栈上的值进行某种特定运算, 并把结果重新存入到操作栈顶。不存在直接支持 byte、short、char 和 boolean 类型的算术指令, 对于上述几种数据的运算, 会使用 int 类型的指令代替。

## 加法

把栈顶的两个数相加:

```
操作码:
        {x}add
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long
- f: float
- d: double

比如: iadd 表示将栈顶两个 int 型数值相加并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 计算 `value1 + value2` 得到 {x} 类型数据 result, 最后 result 被压入到操作数栈中。

## 减法

把栈顶的两个数相减:

```
操作码:
        {x}sub
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long
- f: float
- d: double

比如: isub 表示将栈顶两个 int 型数值相减并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 计算 `value1 - value2` 得到 {x} 类型数据 result, 最后 result 被压入到操作数栈中。

## 乘法

把栈顶的两个数相乘:

```
操作码:
        {x}mul
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long
- f: float
- d: double

比如: imul 表示将栈顶两个 int 型数值相乘并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 计算 `value1 × value2` 得到 {x} 类型数据 result, 最后 result 被压入到操作数栈中。

## 除法

把栈顶的两个数相除:

```
操作码:
        {x}div
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long
- f: float
- d: double

比如: idiv 表示将栈顶两个 int 型数值相除并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 计算 `value1 ÷ value2` 得到结果 result, 然后把 result 转换为 {x} 类型值, 最后 result 被压入到操作数栈中。

## 取余

把栈顶的两个数作取模运算:

```
操作码:
        {x}rem
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long
- f: float
- d: double

比如: irem 表示将栈顶两个 int 型数值作取模运算并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 计算 `value1 - (value1 ÷ value2) × value2` 得到结果 result, 最后 result 被压入到操作数栈中。

## 取反

把栈顶的数取反:

```
操作码:
        {x}neg
操作数:
        -
操作数栈-执行前:
top->   value
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long
- f: float
- d: double

比如: ineg 表示将栈顶 int 型数值取负并将结果压入栈顶。

value 必须为 {x} 类型数据, 指令执行时, value 从操作数栈中出栈, 接着对这个数进行算术取负运算得到结果 result, 最后 result 被压入到操作数栈中。

## 位运算-与

将栈顶两个数值"按位与"并将结果压入栈顶:

```
操作码:
        {x}and
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long

比如: iand 表示将栈顶两 int 型数值"按位与"并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 对这两个数进行按位与操作得到 {x} 类型数据 result, 最后 result 被压入到操作数栈中。

## 位运算-或

```
操作码:
        {x}or
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long

## 位运算-异或

```
操作码:
        {x}xor
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long

## 位运算-左移

将栈顶数值左移指定位数并将结果压入栈顶:

```
操作码:
        {x}shl
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long

比如: ishl 表示将 int 型数值左移指定位数并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 然后将 value1 左移 s 位, 计算后把运算结果入栈回操作数栈中。

s 的取值:

- i: value2 的低 5 位所表示的值
- l: value2 的低 6 位所表示的值

## 位运算-带符号右移

将栈顶数值右移指定位数并将结果压入栈顶:

```
操作码:
        {x}shr
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long

比如: ishr 表示将 int 型数值右移指定位数并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 然后将 value1 右移 s 位, 计算后把运算结果入栈回操作数栈中。

s 的取值:

- i: value2 的低 5 位所表示的值
- l: value2 的低 6 位所表示的值

## 位运算-无符号右移

将栈顶数值右移指定位数并将结果压入栈顶:

```
操作码:
        {x}ushr
操作数:
        -
操作数栈-执行前:
top->   value2
        value1
操作数栈-执行后:
top->   result
```

{x} 需要替换成下面的值的其中之一:

- i: int
- l: long

比如: iushr 表示将 int 型数值右移指定位数并将结果压入栈顶。

value1 和 value2 都必须为 {x} 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 然后将 value1 右移 s 位, 计算后把运算结果入栈回操作数栈中。

s 的取值:

- i: value2 的低 5 位所表示的值
- l: value2 的低 6 位所表示的值

## 自增

将指定 int 型变量增加指定值(如 java 代码: `i++`, `i--`, `i+=2` 等):

```
操作码:
        iinc
操作数:
        index,const
操作数栈-执行前:
top->   -
操作数栈-执行后:
top->   -
```

index 是一个无符号 byte 类型整数, 它作为当前栈帧中局部变量表的索引, const 是一个有符号的 byte 类型值。由 index 定位到的局部变量必须是 int 类型, const 首先带符号扩展成一个 int 类型值, 然后加到由 index 定位到的局部变量中。
