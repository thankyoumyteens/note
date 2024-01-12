# SourceFile 属性

SourceFile 属性用于记录生成这个 Class 文件的源码文件名称, 这个属性也是可选的。在 Java 中, 对于大多数的类来说, 类名和文件名是一致的, 但是有一些特殊情况(如内部类)例外。如果不生成这项属性, 当抛出异常时, 堆栈中将不会显示出错代码所属的文件名。

| 类型 | 名称                 | 数量 |
| ---- | -------------------- | ---- |
| u2   | attribute_name_index | 1    |
| u4   | attribute_length     | 1    |
| u2   | sourcefile_index     | 1    |

sourcefile_index 数据项是指向常量池中 CONSTANT_Utf8_info 型常量的索引, 常量值是源码文件的文件名。

---

![](../../img/class_file10.png)

方法表结束后, 紧接着的 attributes_count`0x0001`, 表示这个 Class 文件有 1 个附加属性。

attribute_name_index 为`0x0010`, 指向常量池中索引为 16 的值`SourceFile`, 说明此属性是这个 Class 文件的源码文件名称。attribute_length 为`0x00000002`。sourcefile_index 为`0x0011`, 指向常量池中索引为 17 的值`ClassFileDemo.java`。

使用 javap -verbose ClassFileDemo.class 命令解析 class 文件:

![](../../img/javap9.png)
