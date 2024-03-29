# 字段

接口索引集合之后，是字段个数(fields_count)和字段集合(fields)。字段集合由字段表(field_info)组成。

字段表(field_info)用于描述接口或者类中声明的字段。Java 语言中的字段(Field)包括类变量和实例变量，但不包括在方法内部声明的局部变量。

## 字段表结构

| 类型           | 名称             | 数量             |
| -------------- | ---------------- | ---------------- |
| u2             | access_flags     | 1                |
| u2             | name_index       | 1                |
| u2             | descriptor_index | 1                |
| u2             | attributes_count | 1                |
| attribute_info | attributes       | attributes_count |

name_index 和 descriptor_index 都是对常量池项的引用，分别代表着字段名以及字段的描述符。

字段集合中不会列出从父类或者父接口中继承而来的字段，但有可能会有编译器自动添加的字段。

## 字段访问标志(access_flags)

| 标志          | 值     | 说明                     |
| ------------- | ------ | ------------------------ |
| ACC_PUBLIC    | 0x0001 | 字段是否 public          |
| ACC_PRIVATE   | 0x0002 | 字段是否 private         |
| ACC_PROTECTED | 0x0004 | 字段是否 protected       |
| ACC_STATIC    | 0x0008 | 字段是否 static          |
| ACC_FINAL     | 0x0010 | 字段是否 final           |
| ACC_VOLATILE  | 0x0040 | 字段是否 volatile        |
| ACC_TRANSIENT | 0x0080 | 字段是否 transient       |
| ACC_SYNTHETIC | 0x1000 | 字段是否由编译器自动产生 |
| ACC_ENUM      | 0x4000 | 字段是否 enum            |

- ACC_PUBLIC、ACC_PRIVATE、ACC_PROTECTED 三个标志最多只能选择其一
- ACC_FINAL、ACC_VOLATILE 不能同时选择
- 接口之中的字段必须有 ACC_PUBLIC、ACC_STATIC、ACC_FINAL 标志

## 字段描述符

| 标识字符 | 说明                           |
| -------- | ------------------------------ |
| B        | 基本类型 byte                  |
| C        | 基本类型 char                  |
| D        | 基本类型 double                |
| F        | 基本类型 float                 |
| I        | 基本类型 int                   |
| J        | 基本类型 long                  |
| S        | 基本类型 short                 |
| Z        | 基本类型 boolean               |
| V        | 特殊类型 void                  |
| L        | 对象类型，如 Ljava/lang/Object |

对于数组类型，每一维度将使用一个前置的`[`字符来描述，如一个 String[][]类型的二维数组将被记录成`[[Ljava/lang/String`，一个整型数组 int[]将被记录成`[I`。

---

```java
public class ClassFileDemo {
    int num;

    public int getNum() {
        return this.num;
    }
}
```

字节码文件内容:

![](../../img/class_file5.png)

字段个数(fields_count)为`0x0001`，即只有一个字段。紧接着是字段集合。

access_flags 为`0x0000`，表示字段没有修饰符。name_index 为`0x0005`，指向常量池中索引为 5 的值`num`。descriptor_index 为`0x0006`，指向常量池中索引为 6 的值`I`。attributes_count 为`0x0000`，表示字段没有额外的属性。

使用 javap -verbose ClassFileDemo.class 命令解析 class 文件，可以对应上字段的内容：

![](../../img/javap4.png)
