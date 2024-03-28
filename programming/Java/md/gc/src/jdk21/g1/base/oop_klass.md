# Oop-Klass 对象模型

一个 Klass 对象代表一个类的元数据。oop 指的是 Ordinary Object Pointer(普通对象指针), 它用来表示一个 Java 对象。

## Klass

Klass 主要提供了两个功能:

1. 用于表示 Java 类。Klass 中保存了一个 Java 对象的类型信息, 包括类名、限定符、常量池、方法字典等。一个 class 文件被 JVM 加载之后, 就会被解析成一个 Klass 对象存储在内存中
2. 保存虚方法表, 用于实现动态分派

JVM 中的 Klass 及其子类:

```cpp
// 用缩进表示继承关系, Klass是下面所有类的父类
class Klass;
//      代表一个普通的Java类
class   InstanceKlass;
//        代表java.lang.Class
class     InstanceMirrorKlass;
//        代表java.lang.ClassLoader
class     InstanceClassLoaderKlass;
//        代表java.lang.ref.Reference及其子类
class     InstanceRefKlass;
//      代表数组类型的Java类, 该Java类是JVM内部自动创建的, 由数组维数和数组基础类型唯一确定
class   ArrayKlass;
//        代表对象类型的数组所对应的类, 比如String[].class
class     ObjArrayKlass;
//        代表Java基础数据类型的一维数组所对应的类, 比如int[].class
class     TypeArrayKlass;
```

当 JVM 加载一个 Java 类时, 它会在内部创建一个对应的 Klass 对象, 用来存放该 Java 类的各种信息。而在 Klass 对象创建过程中, 也会计算该 Java 类所创建的 Java 对象需要多大内存空间, 该计算结果会被保存到 Klass 对象中的\_layout_helper 字段中, 这样当运行时需要创建 Java 对象时, 直接根据这个字段的值分配一块内存就好了。

## oop

一个 Java 对象分为三个部分: 对象头, 实例数据, 对齐填充。

对象头在 JVM 中使用 oopDesc 类表示:

```cpp
class oopDesc {
  // Mark Word
  // 用于存储对象的运行时记录信息,
  // 如哈希值、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID等
  volatile markOop  _mark;
  // 元数据指针
  // 指向一个存储类的元数据的 Klass 对象
  union _metadata {
    // 未压缩的 Klass 指针
    Klass*      _klass;
    // 压缩的 Klass 指针
    narrowKlass _compressed_klass;
  } _metadata;
};
```

oop 在 JVM 中的定义:

```cpp
// 用缩进表示继承关系, oopDesc是下面所有类的父类
//            指向Java对象的指针
typedef class oopDesc* oop;
//              普通Java对象
typedef class   instanceOopDesc* instanceOop;
//              数组对象
typedef class   arrayOopDesc* arrayOop;
//                对象类型的数组
typedef class     objArrayOopDesc* objArrayOop;
//                Java基础数据类型的一维数组
typedef class     typeArrayOopDesc* typeArrayOop;
```

每次 new 一个 Java 对象就时, JVM 就会创建一个新的 oopDesc 对象。
