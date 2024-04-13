# 类型检查指令

## checkcast

检验类型转换, 检验未通过将抛出 ClassCastException

比如下面 java 代码就会生成 checkcast:

```java
Object1 o1 = new Object1();
Object2 o2 = (Object2) o1;
```

```
操作码:
        checkcast
操作数:
        indexbyte1
        indexbyte2
操作数栈-执行前:
top->   objectref
操作数栈-执行后:
top->   objectref
```

objectref 必须为 reference 类型的数据, indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个类、接口或者数组类型的符号引用。

如果 objectref 为 null 的话, 那操作数栈不会有任何变化。否则, 参数指定的类、接口或者数组类型会被 JVM 解析。如果 objectref 可以转换为这个类、接口或者数组类型, 那操作数栈就保持不变, 否则 checkcast 指令将抛出一个 ClassCastException 异常。

假设 S 是 objectref 所指向的对象的类型, T 是进行比较的类型, checkcast 指令根据这些规则来判断转换是否成立:

- 如果 S 是类:
  - 如果 T 也是类, 那 S 必须与 T 是同一个类, 或者 S 是 T 的子类
  - 如果 T 是接口, 那 S 必须实现了 T
- 如果 S 是接口:
  - 如果 T 是类, 那么 T 只能是 Object(接口继承的类只能是 Object)
  - 如果 T 是接口, 那么 T 与 S 应当是相同的接口, 或者 T 是 S 的父接口
- 如果 S 是数组, 假设为 `SC[]` 的形式, 这个数组的组件类型为 SC:
  - 如果 T 是类, 那么 T 只能是 Object
  - 如果 T 是数组, 假设为 `TC[]` 的形式, 这个数组的组件类型为 TC, 那么下面两条规则之一必须成立:
    - TC 和 SC 是同一个原始类型
    - TC 和 SC 都是 reference 类型, 并且 SC 能与 TC 类型相匹配
  - 如果 T 是接口类型, 那 T 必须是数组所实现的接口之一

## instanceof

判断对象是否指定的类型:

```
操作码:
        instanceof
操作数:
        indexbyte1
        indexbyte2
操作数栈-执行前:
top->   objectref
操作数栈-执行后:
top->   result
```

instanceof 指令与 checkcast 指令非常类似, 区别是 instanceof 是返回一个比较结果到操作数栈中。

- 如果 objectref 为 null 的话, instanceof 指令将会把 int 值 0 推入到操作数栈栈顶。
- 如果 objectref 可以转换为指定的类型, 那 instanceof 指令将会把 int 值 1 推入到操作数栈栈顶
- 否则, 如果不能转换, 推入栈顶的就是 int 值 0
