# Buffer

有几个重要属性：capacity（容量）、position（当前位置）、limit（读/写边界）。

常见操作：

- put()：往里写数据
- get()：从中读数据
- flip()：切换到“读模式”(写完准备读的时候必须调用)
- clear() 或 compact()：读完准备再写时用

## Buffer 的使用示例

```java
// 创建 Buffer
ByteBuffer buffer = ByteBuffer.allocate(1024);

// 写入
buffer.put("Hello NIO".getBytes());

// 写完了, 准备读
buffer.flip();

// 读取
int len = buffer.remaining();
byte[] bytes = new byte[len];
buffer.get(bytes);

// 输出
System.out.println(new String(bytes));
```
