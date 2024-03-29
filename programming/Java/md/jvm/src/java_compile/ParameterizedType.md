# 泛型

泛型的本质是参数化类型(Parameterized Type)的应用。

参数化类型将类型由原来的具体的类型参数化，然后在使用时传入具体的类型。在 Java 中，参数化类型使用尖括号(`< >`)实现，如`List<T>`，其中的`T`表示类型参数，在实例化时才会指定具体的类型，如`new ArrayList<Integer>()`。

Java 选择的泛型实现方式叫作类型擦除式泛型(Type Erasure Generics)，而 C#选择的泛型实现方式是具现化式泛型(Reified Generics)。

C#的泛型无论在程序源码里面、编译后的中间语言表示里面，抑或是运行期的 CLR 里面都是切实存在的，`List<int>`与`List<string>`就是两个不同的类型，它们由系统在运行期生成，有着自己独立的虚方法表和类型数据。

而 Java 语言中的泛型则不同，它只在程序源码中存在，在编译后的字节码文件中，全部泛型都被替换为原来的裸类型(Raw Type)，并且在相应的地方插入了强制转型代码，因此对于运行期的 Java 语言来说，`ArrayList<Integer>`与`ArrayList<String>`其实是同一个类型。

```java
// 由于类型擦除，Java中不支持下面的泛型用法
public class TypeErasureGenerics<E> {
    public void doSomething(Object item) {
        // 不合法，无法对泛型进行实例判断
        if (item instanceof E) {}
        // 不合法，无法使用泛型创建对象
        E newItem = new E();
        // 不合法，无法使用泛型创建数组
        E[] itemArray = new E[10];
    }
}
```

Java 的类型擦除式泛型无论在使用效果上还是运行效率上，几乎是全面落后于 C#的具现化式泛型，而它的唯一优点就是可以兼容旧版 JDK，擦除式泛型的实现几乎只需要在 Javac 编译器上做出改进即可，不需要改动字节码、不需要改动 JVM，也保证了以前没有使用泛型的库可以直接运行在新版 JDK 上。

## 类型擦除

由于 Java 选择直接把已有的类型泛型化。比如 ArrayList，原地泛型化后变成了`ArrayList<T>`，而且为了保证以前直接用 ArrayList 的代码在泛型新版本里必须还能继续用这同一个容器，这就必须让所有泛型化的实例类型，比如`ArrayList<Integer>`、`ArrayList<String>`这些全部自动成为 ArrayList 的子类，否则类型转换就是不安全的。

Java 引出了裸类型(Raw Type)的概念，裸类型是所有该类型泛型化实例的共同父类型，比如 ArrayList 就是`ArrayList<T>`的裸类型。

Java 的类型擦除会在编译时把`ArrayList<Integer>`还原回`ArrayList`，只在元素访问、修改时自动插入一些强制类型转换和检查指令。

```java
public static void main(String[] args) {
    Map<String, String> map = new HashMap<String, String>();
    map.put("hello", "你好");
    map.put("how are you?", "吃了没？");
    System.out.println(map.get("hello"));
    System.out.println(map.get("how are you?"));
}
```

把这段 Java 代码编译成 Class 文件，然后再用字节码反编译工具进行反编译后，将会发现泛型都不见了，程序又变回了 Java 泛型出现之前的写法，泛型类型都变回了裸类型，只在元素访问时插入了从 Object 到 String 的强制转型代码：

```java
public static void main(String[] args) {
    Map map = new HashMap();
    map.put("hello", "你好");
    map.put("how are you?", "吃了没？");
    System.out.println((String) map.get("hello"));
    System.out.println((String) map.get("how are you?"));
}
```

对于 int、long 等原始类型(Primitive Types)，一旦把泛型信息擦除后，到要插入强制转型代码的地方就没办法实现了，因为不支持 int、long 与 Object 之间的强制转型。所以 Java 不支持原生类型的泛型，而只能使用`ArrayList<Integer>`、`ArrayList<Long>`等包装类，导致了大量构造包装类和装箱、拆箱的开销。

## 获取参数化类型

由于类型擦除，在运行期无法取到泛型类型信息，会让一些代码变得复杂。

比如下面代码由于不能从 List 中取得参数化类型 T，所以不得不增加一个额外参数，用来传入 T 的类型：

```java
// List转数组
public static <T> T[] listToArray(List<T> list,
                                  Class<T> componentType) {
    // list取不到T的类型
}
```

不过类型擦除仅仅是对方法的 Code 属性中的字节码进行擦除，实际上元数据中还是保留了泛型信息，虽然不能在运行期取到泛型类型信息，但是可以通过反射取得参数化类型。

```java
public class ParameterizedTypeDemo {

    List<String> list = new ArrayList<>();

    public void test(List<Integer> list) {
        System.out.println(list);
    }

    public static void main(String[] args) throws Exception {
        Class<ParameterizedTypeDemo> demoClass = ParameterizedTypeDemo.class;
        // 获取字段的参数化类型
        System.out.println(demoClass.getDeclaredField("list").getGenericType());

        /*
         * 获取方法参数的参数化类型
         */
        Method test = demoClass.getDeclaredMethod("test", List.class);
        // 获取方法的所有参数
        Type[] types = test.getGenericParameterTypes();
        for (Type type : types) {
            // 判断方法参数是否是泛型
            if (type instanceof ParameterizedType) {
                // 取出泛型参数中所有的泛型
                ParameterizedType pt = (ParameterizedType) type;
                Type[] arguments = pt.getActualTypeArguments();
                for (Type paramType : arguments) {
                    System.out.println(paramType);
                }
            }
        }
    }
}
```

运行结果

```
java.util.List<java.lang.String>
class java.lang.Integer
```
