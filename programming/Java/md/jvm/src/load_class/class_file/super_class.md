# 父类索引

父类索引和类索引基本一样, 只不过父类索引是用于确定这个类的父类。

由于 Java 不允许多重继承, 所以父类索引只有一个, 除了 java.lang.Object 之外, 所有 Java 类的父类索引都不为 0。

ClassFileDemo.class 文件中类索引的值是 0x0002, 最终指向了字符串常量"java/lang/Object"。

![](../../img/class_file_sc1.png)

![](../../img/class_file_sc2.png)
