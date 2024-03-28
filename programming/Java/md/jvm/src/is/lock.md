# 同步指令

JVM 可以支持方法级的同步和方法内部一段指令序列的同步, 这两种同步结构都是使用管程(Monitor, 更常见的是直接将它称为"锁")来实现的。

方法级的同步是隐式的, 无须通过字节码指令来控制, 它实现在方法调用和返回操作之中。虚拟机可以从方法常量池中的方法表结构中的 ACC_SYNCHRONIZED 访问标志得知一个方法是否被声明为同步方法。当方法调用时, 调用指令将会检查方法的 ACC_SYNCHRONIZED 访问标志是否被设置, 如果设置了, 执行线程就要求先成功持有管程, 然后才能执行方法, 最后当方法完成(无论是正常完成还是非正常完成)时释放管程。在方法执行期间, 执行线程持有了管程, 其他任何线程都无法再获取到同一个管程。如果一个同步方法执行期间抛出了异常, 并且在方法内部无法处理此异常, 那这个同步方法所持有的管程将在异常抛到同步方法边界之外时自动释放。

同步一段指令集序列通常是由 Java 语言中的 synchronized 语句块来表示的, JVM 的指令集中有 monitorenter 和 monitorexit 两条指令来支持 synchronized 关键字的语义, 正确实现 synchronized 关键字需要 Javac 编译器与 JVM 两者共同协作支持, 编译器必须确保无论方法通过何种方式完成, 方法中调用过的每条 monitorenter 指令都必须有其对
应的 monitorexit 指令, 而无论这个方法是正常结束还是异常结束。

```java
public class App {
    public static final App app = new App();

    public static void main(String[] args) {
        synchronized (app) {
            System.out.println("locked");
        }
    }
}
```

生成的指令如下:

```java
Code:
    stack=2, locals=3, args_size=1
     0: getstatic     #2                  // Field app:Lorg/example/App;
     3: dup
     4: astore_1
     5: monitorenter
     6: getstatic     #3                  // Field java/lang/System.out:Ljava/io/PrintStream;
     9: ldc           #4                  // String locked
    11: invokevirtual #5                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
    14: aload_1
    15: monitorexit
    16: goto          24
    19: astore_2
    20: aload_1
    21: monitorexit
    22: aload_2
    23: athrow
    24: return
    Exception table:
        from    to  target type
            6    16    19   any
           19    22    19   any
```

为了保证在方法异常完成时 monitorenter 和 monitorexit 指令依然可以正确配对执行, 编译器会自动产生一个异常处理程序, 这个异常处理程序声明可处理所有的异常, 它的目的就是用来执行 monitorexit 指令。

## monitorenter

进入一个对象的 monitor

```
操作码:
        monitorenter
操作数:
        -
操作数栈-执行前:
        objectref
操作数栈-执行后:
        -
```

objectref 必须为 reference 类型数据。任何对象都有一个 monitor 与之关联。当且仅当一个 monitor 被持有后, 它
将处于锁定状态。线程执行到 monitorenter 指令时, 将会尝试获取 objectref 所对应的 monitor 的所有权, 那么: 

- 如果 objectref 的 monitor 的进入计数器为 0, 那线程可以成功进入 monitor, 以及将计数器值设置为 1。当前线程就是 monitor 的所有者
- 如果当前线程已经拥有 objectref 的 monitor 的所有权, 那它可以重入这个 monitor, 重入时需将进入计数器的值加 1
- 如果其他线程已经拥有 objectref 的 monitor 的所有权, 那当前线程将被阻塞, 直到 monitor 的进入计数器值变为 0 时, 重新尝试获取 monitor 的所有权

## monitorexit

退出一个对象的 monitor

```
操作码:
        monitorexit
操作数:
        -
操作数栈-执行前:
        objectref
操作数栈-执行后:
        -
```

objectref 必须为 reference 类型数据。执行 monitorexit 指令的线程必须是 objectref 对应的 monitor 的所有
者。指令执行时, 线程把 monitor 的进入计数器值减 1, 如果减 1 后计数器值为 0, 那线程退出 monitor, 不再是这个 monitor 的拥有者。其他被这个 monitor 阻塞的线程可以尝试去获取这个 monitor 的所有权。
