# 操作数栈指令

| 操作码 | 操作数 | 操作数栈-执行前 | 操作数栈-执行后             | 操作                                                    |
| ------ | ------ | --------------- | --------------------------- | ------------------------------------------------------- |
| pop    | -      | value           | -                           | 将栈顶非 long/double 类型的数值弹出                     |
| pop2   | -      | value1,value2   | -                           | 将栈顶的两个非 long/double 类型的数值弹出               |
| pop2   | -      | value           | -                           | 将栈顶的一个 long/double 类型的数值弹出                 |
| dup    | -      | value           | value,value                 | 复制栈顶非 long/double 类型的值并将复制的值压入栈顶     |
| dup2   | -      | value1,value2   | value1,value2,value1,value2 | 复制栈顶两个非 long/double 类型的值并将复制的值压入栈顶 |
| dup2   | -      | value           | value,value                 | 复制栈顶一个 long/double 类型的值并将复制的值压入栈顶   |
| swap   | -      | value1,value2   | value2,value1               | 将栈顶顶的两个非 long/double 类型的值互换               |
