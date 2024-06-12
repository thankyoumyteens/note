# Oop-Klass 对象模型

一个 Klass 对象代表一个 Java 类的元数据。oop 指的是 Ordinary Object Pointer(普通对象指针), 它用来指向一个 Java 对象。

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

oop 在 JVM 中的层级:

```cpp
//////////////////////////////////////////////
// src/hotspot/share/oops/oopsHierarchy.hpp //
//////////////////////////////////////////////

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

## Klass

Klass 主要提供了两个功能:

1. 用于表示 Java 类。Klass 中保存了一个 Java 类的元数据(类型信息, 包括类名、限定符、常量池、方法字典等)。一个 class 文件被 JVM 加载之后, 就会被解析成一个 Klass 对象存储在内存中
2. 保存虚方法表, 用于实现动态分派

```cpp
//////////////////////////////////////
// src/hotspot/share/oops/klass.hpp //
//////////////////////////////////////

class Klass : public Metadata {
 protected:

  // If you add a new field that points to any metaspace object, you
  // must add this field to Klass::metaspace_pointers_do().

  // note: put frequently-used fields together at start of klass structure
  // for better cache behavior (may not make much of a difference but sure won't hurt)
  enum { _primary_super_limit = 8 };

  // The "layout helper" is a combined descriptor of object layout.
  // For klasses which are neither instance nor array, the value is zero.
  //
  // For instances, layout helper is a positive number, the instance size.
  // This size is already passed through align_object_size and scaled to bytes.
  // The low order bit is set if instances of this class cannot be
  // allocated using the fastpath.
  //
  // For arrays, layout helper is a negative number, containing four
  // distinct bytes, as follows:
  //    MSB:[tag, hsz, ebt, log2(esz)]:LSB
  // where:
  //    tag is 0x80 if the elements are oops, 0xC0 if non-oops
  //    hsz is array header size in bytes (i.e., offset of first element)
  //    ebt is the BasicType of the elements
  //    esz is the element size in bytes
  // This packed word is arranged so as to be quickly unpacked by the
  // various fast paths that use the various subfields.
  //
  // The esz bits can be used directly by a SLL instruction, without masking.
  //
  // Note that the array-kind tag looks like 0x00 for instance klasses,
  // since their length in bytes is always less than 24Mb.
  //
  // Final note:  This comes first, immediately after C++ vtable,
  // because it is frequently queried.
  jint        _layout_helper;

  // Klass kind used to resolve the runtime type of the instance.
  //  - Used to implement devirtualized oop closure dispatching.
  //  - Various type checking in the JVM
  // 运行时确定类的实际类型
  // enum KlassKind {
  //   InstanceKlassKind,  普通类
  //   InstanceRefKlassKind, 引用类型(java.lang.ref.Reference的子类, 软引用/弱引用之类的东西)
  //   InstanceMirrorKlassKind, 镜像类
  //   InstanceClassLoaderKlassKind,
  //   InstanceStackChunkKlassKind,
  //   TypeArrayKlassKind, 基本类型的数组类
  //   ObjArrayKlassKind, 对象数组的数组类
  //   UnknownKlassKind
  // };
  const KlassKind _kind;

  // 描述符, 用于java.lang.Class类的getModifiers方法
  // getModifiers方法的作用:
  //  返回指定对象的修饰符(public, protected等)
  jint        _modifier_flags;

  // The fields _super_check_offset, _secondary_super_cache, _secondary_supers
  // and _primary_supers all help make fast subtype checks.  See big discussion
  // in doc/server_compiler/checktype.txt
  //
  // Where to look to observe a supertype (it is &_secondary_super_cache for
  // secondary supers, else is &_primary_supers[depth()].
  juint       _super_check_offset;

  // 类名
  // 普通类, 如: java/lang/String
  // 数组类, 如: [I, [Ljava/lang/String;
  // 其它类: 0
  Symbol*     _name;

  // Cache of last observed secondary supertype
  Klass*      _secondary_super_cache;
  // Array of all secondary supertypes
  Array<Klass*>* _secondary_supers;
  // Ordered list of all primary supertypes
  Klass*      _primary_supers[_primary_super_limit];
  // 指向它的镜像
  OopHandle   _java_mirror;
  // 父类
  Klass*      _super;
  // 子类链表的头节点, 通过next_sibling可以找到下一个子类
  Klass* volatile _subklass;
  // 兄弟类, 父类可以通过这个链表找到所它的有子类
  Klass* volatile _next_sibling;

  // 被同一个类加载器加载的类, 会记录到同一个链表中, 通过这个变量访问
  Klass*      _next_link;

  // 这个类的类加载器
  // 用来访问对应的java.lang.ClassLoader实例
  ClassLoaderData* _class_loader_data;

  int _vtable_len;              // vtable length. This field may be read very often when we
                                // have lots of itable dispatches (e.g., lambdas and streams).
                                // Keep it away from the beginning of a Klass to avoid cacheline
                                // contention that may happen when a nearby object is modified.

  // 类型的访问标志: ACC_PUBLIC, ACC_FINAL, ACC_SUPER, ...
  AccessFlags _access_flags;

};
```

JVM 中 Klass 的层级:

```cpp
//////////////////////////////////////////////
// src/hotspot/share/oops/oopsHierarchy.hpp //
//////////////////////////////////////////////

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

## java_mirror

类加载的最终结果便是在 JVM 的方法区创建一个与 Java 类对应的 instanceKlass 对象，但是 JVM 在创建完 instanceKlass 之后，还会创建这个 instanceKlass 的镜像对象(java_mirror)。instanceKlass 和它的 java_mirror 之间保存了指针来互相访问。

JVM 创建镜像是为了给 Java 程序使用的，而 instanceKlass 则只在 JVM 内部使用。所以，JVM 直接暴露给 Java 的是 java_mirror, 而不是 InstanceKlass。JDK 类库中所提供的反射等工具类，其实都基于 java_mirror 这个内部镜像实现的。
