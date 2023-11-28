# 初始化

初始化(Initialization)阶段是类加载过程的最后一个步骤。之前的几个类加载的阶段, 除了在加载阶段用户可以通过自定义类加载器的方式局部参与外, 其余动作都完全由 Java 虚拟机控制。直到初始化阶段, Java 虚拟机才真正开始执行类中编写的 Java 程序代码, 将主导权移交给应用程序。

初始化阶段就是执行类构造器`<clinit>()`方法的过程。`<clinit>()`是编译器自动生成的。`<clinit>()`方法是由编译器自动收集类中的所有类变量的赋值动作和静态语句块中的语句合并产生的, 编译器收集的顺序是由语句在源代码中出现的顺序决定的, 静态语句块中只能访问到定义在静态语句块之前的变量, 定义在它之后的变量, 在前面的静态语句块可以赋值, 但是不能访问。

Java 虚拟机会保证在子类的`<clinit>()`方法执行前, 父类的`<clinit>()`方法已经执行完毕。第一个执行`<clinit>()`方法的类是 Object 类。

如果一个类中没有静态语句块, 也没有对变量的赋值操作, 那么编译器可以不为这个类生成`<clinit>()`方法。

接口中不能使用静态语句块, 但仍然可以给变量赋初始值, 因此接口也会生成`<clinit>()`方法。但执行接口的`<clinit>()`方法前不需要先执行父接口的`<clinit>()`方法, 因为只有当父接口中定义的变量被使用时, 父接口才会被初始化。此外, 接口的实现类在初始化时也不会执行接口的`<clinit>()`方法。

多个线程同时去初始化一个类时, 只会有其中一个线程去执行这个类的`<clinit>()`方法, 其他线程都需要阻塞等待, 直到活动线程执行完毕`<clinit>()`方法。

## 类的初始化时机

类加载的过程中, 只有初始化阶段的触发时机有明确规定:

1. 遇到`new`、`getstatic`、`putstatic`或`invokestatic`这四条字节码指令时, 如果类型没有进行过初始化, 则需要先触发其初始化阶段。能够生成这四条指令的典型 Java 代码场景有:
   1. 使用 new 关键字创建对象的时候
   2. 读取或设置一个类型的静态字段的时候, 被 static+final 修饰的字段除外
   3. 调用一个类的静态方法的时候
2. 进行反射调用的时候, 如果类型没有进行过初始化, 则需要先触发其初始化
3. 子类被初始化的时候, 如果发现其父类还没有进行过初始化, 则要先初始化其父类
4. 当虚拟机启动时, 会先初始化主类(包含 main 方法的那个类)
5. 当使用 JDK 7 新加入的动态语言支持时, 如果一个 MethodHandle 实例最后的解析结果为 REF_getStatic、REF_putStatic、REF_invokeStatic、REF_newInvokeSpecial 四种类型的方法句柄, 并且这个方法句柄对应的类没有进行过初始化, 则需要先触发其初始化
6. 当一个接口中定义了 JDK 8 新加入的 default 方法时, 如果有这个接口的实现类发生了初始化, 那该接口要在其之前被初始化

这六种场景中的行为称为对一个类型进行主动引用。其他的引用类型的方式都不会触发初始化, 称为被动引用。

## 静态字段的被动引用

对于静态字段, 只有直接定义这个字段的类才会被初始化, 因此通过其子类来引用父类中定义的静态字段, 只会触发父类的初始化而不会触发子类的初始化。

```java
public class SuperClass {
    static {
        System.out.println("SuperClass init!");
    }
    public static int value = 123;
}

public class SubClass extends SuperClass {
    static {
        System.out.println("SubClass init!");
    }
}

public class NotInitialization {
    public static void main(String[] args) {
        // 被动引用, 只会输出SuperClass init!
        System.out.println(SubClass.value);
    }
}
```

## 数组的被动引用

通过数组定义来引用类, 不会触发此类的初始化。但是这段代码里面触发了另一个名为 \[Lcom.example.SuperClass 的类的初始化阶段, 这不是一个合法的类名, 它是一个由虚拟机自动生成的、直接继承于 java.lang.Object 的子类, 创建动作由字节码指令 newarray 触发。

```java
public class SuperClass {
    static {
        System.out.println("SuperClass init!");
    }
}

public class NotInitialization {
    public static void main(String[] args) {
        // 被动引用, 没有输出
        // 被初始化的是数组类: [Lcom.example.SuperClass
        SuperClass[] sca = new SuperClass[10];
    }
}
```

## 常量的被动引用

常量在编译阶段会直接存入调用类的常量池中, 本质上没有直接引用到定义常量的类, 因此不会触发定义常量的类的初始化。

比如, 虽然在 NotInitialization 类中引用了 ConstClass 类的常量 HELLOWORLD, 但经过编译阶段的优化, 已经将此常量的值"hello world"直接存储在 NotInitialization 类的常量池中, 以后 NotInitialization 对常量 ConstClass.HELLOWORLD 的引用, 实际都被转化为 NotInitialization 类对自身常量池的引用了。NotInitialization 的 Class 文件之中并没有 ConstClass 类的符号引用入口, 这两个类在编译成 Class 文件后就已不存在任何联系了。

```java
public static class ConstClass {
    static {
        System.out.println("ConstClass init!");
    }
    public static final String HELLOWORLD = "hello world";
}

public class NotInitialization {
    public static void main(String[] args) {
        // 被动引用, 没有输出
        System.out.println(ConstClass.HELLOWORLD);
    }
}
```

## 接口的初始化时机

接口也有初始化过程, 接口中不能使用 static 语句块, 但编译器会为接口生成`<clinit>()`方法, 用于初始化接口中所定义的成员变量。

接口与类触发初始化的时机基本相同, 唯一不同的地方是接口在初始化时, 并不要求其父接口全部都完成了初始化, 只有在真正使用到父接口的时候才会初始化其父接口。
