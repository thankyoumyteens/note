# JOL 工具

openjdk 官网提供了查看对象内存布局的工具 jol (java object layout)。

## 用法

1. 导入依赖: 

```xml
<dependency>
    <groupId>org.openjdk.jol</groupId>
    <artifactId>jol-core</artifactId>
    <version>0.17</version>
</dependency>
```

2. 测试类: 

```java
public class DemoObj {
    public boolean val1;
    public int val2;
    public String val3;
}
```

3. 打印 DemoObj 类的对象的内存布局: 

```java
DemoObj obj = new DemoObj();
obj.val1 = true;
obj.val2 = 100;
obj.val3 = "str";
System.out.println(ClassLayout.parseInstance(obj).toPrintable());
```

4. 输出: 

```java
demo.DemoObj object internals:
OFF  SZ               TYPE DESCRIPTION               VALUE
  0   8                    (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4                    (object header: class)    0xf800c146
 12   4                int DemoObj.val2              100
 16   1            boolean DemoObj.val1              true
 17   3                    (alignment/padding gap)
 20   4   java.lang.String DemoObj.val3              (object)
Instance size: 24 bytes
Space losses: 3 bytes internal + 0 bytes external = 3 bytes total
```

输出结果中每一列的含义: 

1. OFF: 偏移量
2. SZ: 占用字节数
3. TYPE: Java 类型
4. DESCRIPTION: 描述
5. VALUE: 值
