# 类加载器的可见性

默认情况下, 类加载器之间不是相互可见的。也就是说, 一个类加载器加载的类对于另一个类加载器来说是不可见的, 除非它们存在父子关系（即一个加载器是另一个加载器的父加载器）。子类的加载器可以看见所有的父类加载器加载的类, 而父类加载器看不到子类加载器加载的类。

要让一个类加载器加载的类对其他类加载器可见, 通常有以下几种方法: 

1. **使用相同的类加载器**: 
   最简单的方法是确保所有相关类都使用同一个类加载器来加载。这可以通过在创建类实例时显式指定类加载器来实现。

2. **使用双亲委派模型**: 
   利用 Java 的双亲委派模型, 子类加载器可以访问其父类加载器加载的类。这意味着如果你有一个类加载器的层次结构, 那么子加载器可以访问父加载器加载的类。

3. **使用代理类**: 
   如果两个类由不同的类加载器加载, 并且无法改变加载器, 你可以通过创建一个共享的代理类来间接访问这些类。代理类可以由两个类加载器都能访问的类加载器加载。

## 示例

```java
public class Demo {

    public Class<?> getPerson(ClassLoader c) throws Exception {
        return Class.forName("org.example.Person", true, c);
    }
}

public class App {

    static class MyClassLoader extends ClassLoader {

        public MyClassLoader(ClassLoader parent) {
            super(parent);
        }

        public Class<?> load(String fullClassName, byte[] b) {
            return defineClass(fullClassName, b, 0, b.length);
        }
    }

    public static void main(String[] args) throws Exception {
        MyClassLoader parentClassLoader = new MyClassLoader(App.class.getClassLoader());
        MyClassLoader classLoader = new MyClassLoader(parentClassLoader);
        MyClassLoader siblingClassLoader = new MyClassLoader(parentClassLoader);
        MyClassLoader subClassLoader = new MyClassLoader(classLoader);

        byte[] bytes = AsmDemo.genClass();
        Class<?> clazz = classLoader.load("org.example.Person", bytes);
        System.out.println("ASM动态创建的Person类已经加载进JVM => " + clazz);

        Demo demo = new Demo();

        try {
            System.out.println("父类加载器不能访问子类加载器加载的class => " + demo.getPerson(parentClassLoader));
        } catch (Exception e) {
            System.out.println("父类加载器不能访问子类加载器加载的class => " + e);
        }
        try {
            System.out.println("类加载器可以访问自己加载的class => " + demo.getPerson(classLoader));
        } catch (Exception ignored) {
        }
        try {
            System.out.println("同级类加载器不能访问同级类加载器加载的class => " + demo.getPerson(siblingClassLoader));
        } catch (Exception e) {
            System.out.println("同级类加载器不能访问同级类加载器加载的class => " + e);
        }
        try {
            System.out.println("子类加载器可以访问父类加载器加载的class => " + demo.getPerson(subClassLoader));
        } catch (Exception ignored) {
        }
    }
}
```

输出:

```
ASM动态创建的Person类已经加载进JVM => class org.example.Person
父类加载器不能访问子类加载器加载的class => java.lang.ClassNotFoundException: org.example.Person
类加载器可以访问自己加载的class => class org.example.Person
同级类加载器不能访问同级类加载器加载的class => java.lang.ClassNotFoundException: org.example.Person
子类加载器可以访问父类加载器加载的class => class org.example.Person
```
