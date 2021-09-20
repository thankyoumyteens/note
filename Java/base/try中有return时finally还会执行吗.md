# try中有return时finally还会执行吗

```java
public class FinallyTest {
    public int method() {
        int x = 1;
        try{
            ++ x;
            return x;
        }catch(Exception e){

        }finally{
            ++ x;
        }
        return x;
    }

    public static void main(String[] args) {
        FinallyTest t = new FinallyTest();
        int y = t.method();
        System.out.println(y);
    }
}
```

对于上述代码，我们有以下几个问题，来自测一下吧：

- 如果在 try 语句块里使用 return 语句，那么 finally 语句块还会执行吗？
- 如果执行，那么是怎样实现既执行 return 又执行 finally 的呢？
- 上面的程序输出是什么？为什么？

Java官方文档上是这么描述的:

The finally block always executes when the try block exits.`

我们看到描述词用的是always，即在try执行完成之后，finally是一定会执行的。

这种特性可以让程序员避免在try语句中使用了return, continue或者 break关键字而忽略了关闭相关资源的操作。

把清理相关资源放到finally语句块中一直是最佳实践。

我们知道了finally语句会执行，当我们在IDE上运行该程序的时候，会发现运行结果是2。那么为什么不是3呢？

原来JVM规范里面明确说明了这种情况：

If the try clause executes a return, the compiled code does the following:

1. Saves the return value (if any) in a local variable.
2. Executes a jsr to the code for the finally clause.
3. Upon return from the finally clause, returns the value saved in the local variable.

大意就是如果在try中return的情况下，先把try中将要return的值先存到一个本地变量中，即本例中的x=2将会被保存下来。接下来去执行finally语句，最后返回的是存在本地变量中的值，即返回x=2.

Notes:还有一点要注意的，如果你在finally里也用了return语句，比如return ++x。那么程序返回值会是3。因为规范规定了，当try和finally里都有return时，会忽略try的return，而使用finally的return。

总结

try中有return, 会先将值暂存，无论finally语句中对该值做什么处理，最终返回的都是try语句中的暂存值。
当try与finally语句中均有return语句，会忽略try中return。
