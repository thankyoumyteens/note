# 显式异常处理表

Code 属性表中，在字节码指令之后的是这个方法的显式异常处理表 exception_table，异常表对于 Code 属性来说并不是必须存在的。

显式异常处理表结构：

| 类型 | 名称       | 数量 |
| ---- | ---------- | ---- |
| u2   | start_pc   | 1    |
| u2   | end_pc     | 1    |
| u2   | handler_pc | 1    |
| u2   | catch_type | 1    |

catch_type 为指向一个 CONSTANT_Class_info 型常量的索引。

如果当字节码从第 start_pc 行到第 end_pc 行之间(不含第 end_pc 行)出现了类型为 catch_type 或者其子类的异常，则转到第 handler_pc 行继续处理。当 catch_type 的值为 0 时，代表任意异常情况都需要转到 handler_pc 处进行处理。

```java
public class ExceptionTableDemo {
    public int inc() {
        int x;
        try {
            x = 1;
            return x;
        } catch (Exception e) {
            x = 2;
            return x;
        } finally {
            x = 3;
        }
    }
}
```

如果没有出现异常，返回值是 1。如果出现了 Exception 异常，返回值是 2。如果出现了 Exception 以外的异常，方法非正常退出，没有返回值。

使用`javap -verbose ExceptionTableDemo.class`命令解析 class 文件：

![](../../img/etd.png)

字节码中第 0 到 3 行所做的操作就是将整数 1 赋值给变量 x，并且将此时 x 的值复制一份副本到本地变量表的变量槽中，这个变量槽里面的值在 ireturn 指令执行前将会被重新读到操作栈顶，作为方法返回值使用。

如果这时候没有出现异常，则会继续执行第 4 到 7 行，将变量 x 赋值为 3，然后将之前保存的返回值 1 读入到操作栈顶，最后 ireturn 指令会以 int 形式返回操作栈顶中的值，方法结束。

如果出现了 Exception 异常，程序计数器指针转到第 8 行，第 8 到 16 行所做的事情是将 2 赋值给变量 x，然后将变量 x 此时的值存储为返回值，最后再将变量 x 的值改为 3。方法返回前同样将返回值 2 读到了操作栈顶。

如果出现了 Exception 以外的异常，程序计数器指针转到第 17 行代码，将变量 x 的值赋为 3，并将栈顶的异常抛出，方法结束。
