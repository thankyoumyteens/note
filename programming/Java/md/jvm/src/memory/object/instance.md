# 实例数据

实例数据(Instance Data)保存的是对象中的字段内容, 如果有继承关系存在, 子类还会包含从父类继承过来的字段。

各类型的字段占用的空间大小:

- byte、boolean -> 1 字节
- char、short -> 2 字节
- int、float -> 4 字节
- long、double -> 8 字节
- 引用类型 -> 不开启指针压缩 8 字节, 开启指针压缩 4 字节

## 字段重排序

字段在内存中的排列顺序与在类中定义的顺序不一定相同, JVM 会使用字段重排序技术, 对原始类型进行重新排序, 以达到内存对齐的目的。

1. 按照字段类型的大小, 从大到小排列
2. 具有相同大小的字段, 会被分配在相邻位置
3. 如果一个字段的长度是 L 个字节, 那么这个字段的偏移量(OFFSET)需要对齐至 nL(n 为整数)。比如 long 类型占 8 字节, 所以它的偏移量是 8n, 再加上对象头占 12 字节, 所以 long 类型字段的最小偏移量是 16
4. 当对象头不是 8 字节的整数倍时, 会按从大到小的顺序, 使用 4、2、1 字节的字段进行补位, 字段的排序可能会打破第 1 条规则
5. 默认情况下, 基本数据类型的字段排在引用类型之前, 可以使用参数 -XX:FieldsAllocationStyle=0 让引用类型排在前面

```java
public class DemoObj {

    byte v1;
    char v2;
    long v3;

    public static void main(String[] args) throws InterruptedException {
        DemoObj obj = new DemoObj();
        System.out.println(ClassLayout.parseInstance(obj).toPrintable());

    }
}
```

输出:

```java
demo.DemoObj object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4        (object header: class)    0xf800c105
 12   2   char DemoObj.v2
 14   1   byte DemoObj.v1                0
 15   1        (alignment/padding gap)
 16   8   long DemoObj.v3                0
Instance size: 24 bytes
Space losses: 1 bytes internal + 0 bytes external = 1 bytes total
```

对象头占 12 字节, 由于不是 8 的整数倍, 所以需要找一个合适的字段进行补位, 按照顺序使用 char 类型字段 v2 补位, 补位后还是不够, 继续用 byte 类型的字段 v1 补位, 虽然仍然不够 8 的整数倍, 但是可以补位的字段都用完了。接下来的字段按照从大到小的顺序进行排列, 由于 long 类型最小偏移量是 16, 所以也需要在 long 类型前面填充 1 字节, 使 long 类型字段 v3 的偏移量达到 16。

## 存在父类时的字段重排序

当一个类拥有父类时, 整体遵循父类的字段出现在子类的字段之前。

```java
public class DemoObj {

    byte v1;
    char v2;
    long v3;

    public static class DemoChild extends DemoObj {
        byte v4;
        char v5;
    }

    public static void main(String[] args) throws InterruptedException {
        DemoChild obj = new DemoChild();
        System.out.println(ClassLayout.parseInstance(obj).toPrintable());

    }
}
```

输出:

```java
demo.DemoObj$DemoChild object internals:
OFF  SZ   TYPE DESCRIPTION               VALUE
  0   8        (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4        (object header: class)    0xf800c146
 12   2   char DemoObj.v2
 14   1   byte DemoObj.v1                0
 15   1        (alignment/padding gap)
 16   8   long DemoObj.v3                0
 24   2   char DemoChild.v5
 26   1   byte DemoChild.v4              0
 27   5        (object alignment gap)
Instance size: 32 bytes
Space losses: 1 bytes internal + 5 bytes external = 6 bytes total
```
