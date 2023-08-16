# JVM预定义属性

| 属性名称 | 使用位置 | 含义 |
| -- | -- | -- |
| Code | 方法表中 | Java代码编译成的字节码指令(即：具体的方法逻辑字节码指令) |
| ConstantValue | 字段表中 | final关键字定义的常量值 |
| Deprecated | 类中、方法表中、字段表中 | 被声明为deprecated的方法和字段 |
| Exceptions | 方法表中 | 方法声明的异常 |
| LocalVariableTable | Code属性中 | 方法的局部变量描述 |
| LocalVariableTypeTable | 类中 | JDK1.5中新增的属性，它使用特征签名代替描述符，是为了引入泛型语法之后能描述泛型参数化类型而添加 |
| InnerClasses | 类中 | 内部类列表 |
| EnclosingMethod | 类中 | 仅当一个类为局部类或者匿名类时，才能拥有这个属性，这个属性用于表示这个类所在的外围方法 |
| LineNumberTable | Code属性中 | Java源码的行号与字节码指令的对应关系 |
| StackMapTable | Code属性中 | JDK1.6中新增的属性，供新的类型检查验证器(Type Checker)检查和处理目标方法的局部变量和操作数栈所需要的类型是否匹配 |
| Signature | 类中、方法表中、字段表中 | JDK1.5新增的属性，这个属性用于支持泛型情况下的方法签名，在Java语言中，任何类、接口、初始化方法或成员的泛型签名如果包含了类型变量(Type Variables)或参数类型(Parameterized Types),则Signature属性会为它记录泛型签名信息。由于Java的泛型采用擦除法实现，在为了避免类型信息被擦除后导致签名混乱，需要这个属性记录泛型中的相关信息 |
| SourceFile | 类中 | 记录源文件名称 |
| SourceDebugExtension | 类中 | JDK1.6中新增的属性，SourceDebugExtension用于存储额外的调试信息。如在进行JSP文件调试时，无法通过Java堆栈来定位到JSP文件的行号，JSR-45规范为这些非Java语言编写，却需要编译成字节码运行在Java虚拟机汇中的程序提供了一个进行调试的标准机制，使用SourceDebugExtension就可以存储这些调试信息。 |
| Synthetic | 类中、方法表中、字段表中 | 标识方法或字段为编译器自动产生的 |
| RuntimeVisibleAnnotations | 类中、方法表中、字段表中 | JDK1.5中新增的属性，为动态注解提供支持。RuntimeVisibleAnnotations属性，用于指明哪些注解是运行时(实际上运行时就是进行反射调用)可见的。 |
| RuntimeInvisibleAnnotations | 类中、方法表中、字段表中 | JDK1.5中新增的属性，作用与RuntimeVisibleAnnotations相反用于指明哪些注解是运行时不可见的。 |
| RuntimeVisibleParameterAnnotations | 方法表中 | JDK1.5中新增的属性，作用与RuntimeVisibleAnnotations类似，只不过作用对象为方法的参数。 |
| RuntimeInvisibleParameterAnnotations | 方法表中 | JDK1.5中新增的属性，作用与RuntimeInvisibleAnnotations类似，只不过作用对象为方法的参数。 |
| AnnotationDefault | 方法表中 | JDK1.5中新增的属性，用于记录注解类元素的默认值 |
| BootstrapMethods | 类中 | JDK1.7新增的属性，用于保存invokedynamic指令引用的引导方法限定符 |
| RuntimeVisibIeTypeAnnotations | 类、方法表 、字段表、Code 属性 | JDK8中新增的属性，为实现JSR 308中新增的类型注解提供的支持，用于指明哪些类注解是运行时(实际上运行时就是进行反射调用)可见的 |
| RuntimeInvisibIeTypeAnnotations | 类、方法表 、字段表、Code 属性 | JDK8中新增的属性，为实现JSR 308中新增的类型注解提供的支持，与RuntimeVisibIeTypeAnnotations属性作用刚好相反，用于指明哪些注解是运行时不可见的 |
| MethodParameters | 方法表 | JDK8中新增的属性，用于支持(编译时加上-parameters参数)将方法名称编译进Class文件中，并可运行时获取。此前要获取方法名称(典型的如IDE 的代码提示)只能通过JavaDoc中得到 |
| Module | 类 | JDK9中新增的属性，用于记录一个Module的名称以及相关信息(requires、exports、opens、uses、provides) |
| ModuIePackages | 类 | JDK9中新增的属性，用于记录一个模块中所有被exports或者opens的包 |
| ModuleMainClass | 类 | JDK9中新增的属性，用于指定一个模块的主类 |
| NestHost | 类 | JDK11中新增的属性，用于支持嵌套类(Java中的内部类)的反射和访问控制的API，一个内部类通过该属性得知自己的宿主类 |
| NestMembers | 类 | JDK11中新增的属性，用于支持嵌套类(Java中的内部类)的反射和访问控制的API，一个宿主类通过该属性得知自己有哪些内部类 |

## SourceDebugExtension

为了方便在编译器和动态生成的Class中加入供程序员使用的自定义内容，在JDK 5时，新增了SourceDebugExtension属性用于存储额外的代码调试信息。典型的场景是在进行JSP文件调试时，无法通过Java堆栈来定位到JSP文件的行号。JSR 45提案为这些非Java语言编写，却需要编译成字节码并运行在Java虚拟机中的程序提供了一个进行调试的标准机制，使用SourceDebugExtension属性就可以用于存储这个标准所新加入的调试信息，比如让程序员能够快速从异常堆栈中定位出原始JSP中出现问题的行号。

| 类型 | 名称                            | 数量 |
| ---- | --------------------------------- | ---- |
| u2   | attribute_name_index              | 1    |
| u4   | attribute_length                  | 1    |
| u1   | debug_extension\[attribute_length\] | 1    |

debug_extension存储的就是额外的调试信息，是一组通过变长UTF-8格式来表示的字符串。一个类中最多只允许存在一个SourceDebugExtension属性。

## ConstantValue

ConstantValue属性的作用是通知虚拟机自动为静态变量赋值。只有被static关键字修饰的变量才可以使用这项属性。对非static类型的变量的赋值是在实例构造器`<init>()`方法中进行的。而对于类变量，则有两种方式可以选择：在类构造器`<clinit>()`方法中或者使用ConstantValue属性。

目前Oracle公司实现的Javac编译器的选择是，如果同时使用final和static来修饰一个变量，并且这个变量的数据类型是基本类型或者java.lang.String的话，就将会生成ConstantValue属性来进行初始化。如果这个变量没有被final修饰，或者并非基本类型及字符串，则将会选择在`<clinit>()`方法中进行初始化。

| 类型 | 名称               | 数量 |
| ---- | -------------------- | ---- |
| u2   | attribute_name_index | 1    |
| u4   | attribute_length     | 1    |
| u2   | constantvalue_index  | 1    |

constantvalue_index数据项代表了常量池中一个字面量常量的引用，根据字段类型的不同，字面量可以是CONSTANT_Long_info、CONSTANT_Float_info、CONSTANT_Double_info、CONSTANT_Integer_info和CONSTANT_String_info常量中的一种。

## InnerClasses

InnerClasses属性用于记录内部类与宿主类之间的关联。如果一个类中定义了内部类，那编译器将会为它以及它所包含的内部类生成InnerClasses属性。

