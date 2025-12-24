# 描述符

- 基本类型：
  - `I`：int
  - `J`：long
  - `Z`：boolean
  - `F`：float
  - `D`：double
  - `V`：void
- 引用类型：
  - `Ljava/lang/String;`: java.lang.String
  - `Ljava/util/List;`: java.util.List
- 数组：
  - `[I`: int 数组
  - `[Ljava/lang/String;`: String 数组
- 方法描述符：(参数类型...)返回类型
  - `()V`：无参，返回 `void`
  - `(I)I`：一个 `int` 参数，返回 `int`
  - `(Ljava/lang/String;I)V`：`(String, int) -> void`
  - `([I)V`：一个 `int[]` 参数，返回 `void`

常配合 Type 工具类用：

```java
Type.getDescriptor(String.class); // Ljava/lang/String;
Type.getMethodDescriptor(Type.INT_TYPE, Type.INT_TYPE, Type.INT_TYPE); // (II)I
```
