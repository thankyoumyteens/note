# Klass

klass 用来在 JVM 层表示 Java 类。它的所有成员可以包含虚拟机内部运行一个 Java 类所需的所有信息。

Klass 主要提供了两个功能:

1. klass 提供一个与 Java 类对等的 C++ 类型描述。Klass 中保存了一个 Java 类的元数据(类型信息, 包括类名、限定符、常量池等)。一个 class 文件被 JVM 加载之后, 就会被解析成一个 Klass 对象存储在内存中
2. klass 提供 JVM 内部的函数分发机制。klass 会保存虚方法表, 用于在运行期找到真正要执行的函数

JVM 中 Klass 的层级:

```cpp
// --- src/hotspot/share/oops/oopsHierarchy.hpp --- //

// 用缩进表示继承关系, Klass是下面所有类的父类
class Klass;
class   InstanceKlass; // 一个普通的Java类
class     InstanceMirrorKlass; // java.lang.Class
class     InstanceClassLoaderKlass; // java.lang.ClassLoader
class     InstanceRefKlass; // java.lang.ref.Reference及其子类
class     InstanceStackChunkKlass; // 栈块类型
class   ArrayKlass; // 数组类型的Java类, 该Java类是JVM内部自动创建的, 由数组维数和数组基础类型唯一确定
class     ObjArrayKlass; // 对象类型的数组所对应的类, 比如String[].class
class     TypeArrayKlass; // Java基础数据类型的一维数组所对应的类, 比如int[].class
```

当 JVM 加载一个 Java 类时, 它会在内部创建一个对应的 Klass 对象, 用来存放该 Java 类的各种信息。而在 Klass 对象创建过程中, 也会计算该 Java 类所创建的 Java 对象需要多大内存空间, 该计算结果会被保存到 Klass 对象的 `_layout_helper` 变量中, 这样当运行时需要创建 Java 对象时, 直接根据这个字段的值分配一块内存就好了。

```cpp
// --- src/hotspot/share/oops/klass.hpp --- //

class Klass : public Metadata {
    // If you add a new field that points to any metaspace object, you
    // must add this field to Klass::metaspace_pointers_do().

    // note: put frequently-used fields together at start of klass structure
    // for better cache behavior (may not make much of a difference but sure won't hurt)
    enum {
        _primary_super_limit = 8
    };

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
    // _layout_helper使用4个字节存储
    //
    // 如果是一个普通对象, _layout_helper的值是正数, 表示对象需要占用的内存大小
    // 如果这个对象不支持快速分配(在TLAB里分配), 那么它的低位比特会被设置成特殊的值
    //
    // 如果是一个数组, _layout_helper的值是负数
    // 其4个字节的布局如下:
    //    最高有效位:[tag, hsz, ebt, log2(esz)]:最低有效位
    // 每个字节的含义:
    //    tag: 如果值为 0x80 则表示数据元素是对象, 如果值为 0xC0 则表示数组元素是基本类型
    //    hsz 数组头的大小(单位是字节), 同时指明数组的第一个元素应该偏移多少
    //    ebt 数组元素是基本类型的话, 它表示具体是哪个类型
    //    esz 数组元素的大小(单位是字节)
    jint _layout_helper;

    // 运行时确定类的实际类型
    //  - 用来实现去虚拟化
    //  - JVM中的各种类型检查
    // 在面向对象编程中，多态通常通过虚函数（或称虚方法）实现。
    // 当一个类的方法被声明为虚方法时，这个方法的调用是在运行时根据对象的实际类型来决定的，这称为动态绑定或动态调度。
    // 然而，这种灵活性是以性能为代价的，因为每次调用都需要查找虚函数表（vtable）来确定实际要调用的方法。
    // 去虚拟化是一种编译器优化技术，它尝试在编译时静态地确定方法调用的目标，从而避免运行时的虚函数表查找。
    // 如果编译器能够证明某个特定的对象总是属于某个具体的类，那么它可以将虚方法调用转换为直接调用，提高执行效率。
    // enum KlassKind {
    //     InstanceKlassKind, // 普通类
    //     InstanceRefKlassKind, // 引用类型(java.lang.ref.Reference的子类)
    //     InstanceMirrorKlassKind, // 镜像类型(java.lang.Class)
    //     InstanceClassLoaderKlassKind, // 类加载器类型(java.lang.ClassLoader)
    //     InstanceStackChunkKlassKind, // 栈块类型
    //     TypeArrayKlassKind, // 基本类型数组
    //     ObjArrayKlassKind, // 对象数组
    //     UnknownKlassKind // 未知类型
    // };
    const KlassKind _kind;

    // 类的描述符, 用于java.lang.Class类的getModifiers方法
    // getModifiers方法的作用: 返回类的描述符(public, protected, private, final, static, abstract, interface)
    jint _modifier_flags;

    // The fields _super_check_offset, _secondary_super_cache, _secondary_supers
    // and _primary_supers all help make fast subtype checks.  See big discussion
    // in doc/server_compiler/checktype.txt
    //
    // Where to look to observe a supertype (it is &_secondary_super_cache for
    // secondary supers, else is &_primary_supers[depth()].
    juint _super_check_offset;

    // 类名
    // 普通类, 如: java/lang/String
    // 数组类, 如: [I, [Ljava/lang/String;
    // 其它类: 0
    Symbol *_name;

    // Cache of last observed secondary supertype
    Klass *_secondary_super_cache;
    // Array of all secondary supertypes
    Array<Klass *> *_secondary_supers;
    // Ordered list of all primary supertypes
    Klass *_primary_supers[_primary_super_limit];
    // 当前类的镜像, 对应 java.lang.Class
    OopHandle _java_mirror;
    // 父类
    Klass *_super;
    // 子类链表的头节点, 通过_subklass->next_sibling()可以找到下一个子类
    Klass *volatile _subklass;
    // 兄弟类, 父类可以通过这个链表找到所它的有子类
    Klass *volatile _next_sibling;

    // 被同一个类加载器加载的类, 会记录到同一个链表中, 通过这个变量访问
    Klass *_next_link;

    // 这个类的类加载器
    // 用来访问对应的java.lang.ClassLoader实例
    ClassLoaderData *_class_loader_data;

    int _vtable_len;              // vtable length. This field may be read very often when we
    // have lots of itable dispatches (e.g., lambdas and streams).
    // Keep it away from the beginning of a Klass to avoid cacheline
    // contention that may happen when a nearby object is modified.
    // 类型的访问标志: ACC_PUBLIC, ACC_FINAL, ACC_SUPER, ...
    AccessFlags _access_flags;    // Access flags. The class/interface distinction is stored here.
};
```

## java_mirror

类加载的最终结果便是在 JVM 的方法区创建一个与 Java 类对应的 instanceKlass 对象, 但是 JVM 在创建完 instanceKlass 之后, 还会创建这个 instanceKlass 的镜像对象(java_mirror)。instanceKlass 和它的 java_mirror 之间保存了指针来互相访问。

JVM 创建镜像是为了给 Java 程序使用的, 而 instanceKlass 则只在 JVM 内部使用。所以, JVM 直接暴露给 Java 的是 java_mirror, 而不是 InstanceKlass。JDK 类库中所提供的反射等工具类, 其实都基于 java_mirror 这个内部镜像实现的。
