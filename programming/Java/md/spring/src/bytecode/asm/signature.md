# 泛型

普通的类的描述符格式是`L类的内部名;`, 比如`Ljava/lang/Object;`。泛型的描述符格式是`T泛型名称;`, 比如`TT;`, `TE;`。

泛型要求必须继承于一个确切的类, 对于没有写 extends 限定的泛型, 它们默认继承于 Object。比如`public <T> void test(List<T> list)`, 泛型 T 就是继承于 Object。

## 泛型的声明

在字节码中, 泛型的声明要用尖括号包上。每个泛型都包含一个(或两个)冒号, 冒号前方是类型参数名称, 后方是类型参数的超类或另一个已声明的类型参数。如果类型参数继承于一个接口, 那么应该使用双冒号。

比如泛型:

```java
<T extends Serializable, R extends T>
```

它的声明如下:

```java
// 首先是类型T的声明
// T继承的是接口Serializable, 所以要用::
// 接着是类型R的声明
// T继承的是泛型T, T的描述符是: TT;
// T不是接口, , 所以要用:
<T::Ljava/io/Serializable;R:TT;>
```

## 泛型签名

泛型签名与修饰的结构有关。

### 方法的泛型签名

方法的泛型签名类似普通的方法描述符, 只是要在前面加上泛型声明(如果有的话), 以及在方法描述符中加上泛型。如果方法带有抛出异常声明并且异常列表含有泛型, 那么在描述符之后还要加上异常列表。异常列表的每个类都要用^开头并且需要写出具体的泛型信息。

比如下面的方法:

```java
public <T extends Serializable, E extends Exception> void test(List<T> list) throws E {
    for (T t : list) {
        System.out.println(t);
    }
}
```

字节码如下:

```java
public <T extends java.io.Serializable, E extends java.lang.Exception> void test(java.util.List<T>) throws E;
  descriptor: (Ljava/util/List;)V
  flags: (0x0001) ACC_PUBLIC
  Code:
    // 省略
  Signature: #34  // <T::Ljava/io/Serializable;E:Ljava/lang/Exception;>(Ljava/util/List<TT;>;)V^TE;
```

其中 Signature 指向的字符串常量就是泛型的签名:

```java
// 泛型的声明: <T::Ljava/io/Serializable;E:Ljava/lang/Exception;>
// 带泛型的方法描述符: (Ljava/util/List<TT;>;)V
// 抛出的异常类型: ^TE;
<T::Ljava/io/Serializable;E:Ljava/lang/Exception;>(Ljava/util/List<TT;>;)V^TE;
```

来看另一个方法:

```java
public <T> void test(List<T> list) throws Exception {
    for (T t : list) {
        System.out.println(t);
    }
}
```

它的泛型签名:

```java
// 泛型的声明: <T:Ljava/lang/Object;>
// 带泛型的方法描述符: (Ljava/util/List<TT;>;)V
// 抛出的异常不包含泛型
<T:Ljava/lang/Object;>(Ljava/util/List<TT;>;)V
```

没有定义泛型的方法:

```java
public void test(List<Integer> list) {
    for (Integer t : list) {
        System.out.println(t);
    }
}
```

它的泛型签名:

```java
// 泛型的声明: 由于这个方法没有定义自己的泛型, 所以不包含泛型的声明
// 带泛型的方法描述符: (Ljava/util/List<Ljava/lang/Integer;>;)V
(Ljava/util/List<Ljava/lang/Integer;>;)V
```

### 类和字段的泛型签名

类的泛型签名包括泛型的声明, 以及父类和接口的描述符。

字段不能自己定义泛型, 只能使用类的泛型, 所以泛型签名只包含它的类型的泛型信息。

```java
public class MyList<T> implements List<T> {

    public List<T> copy;

    // 省略
}
```

类的泛型签名:

```java
// 泛型的声明: <T:Ljava/lang/Object;>
// 父类的描述符: Ljava/lang/Object;
// 接口的描述符: Ljava/util/List<TT;>;
<T:Ljava/lang/Object;>Ljava/lang/Object;Ljava/util/List<TT;>;
```

字段的泛型签名:

```java
Ljava/util/List<TT;>;
```

## 在 ASM 中使用泛型

```java
// public <T> void test(List<T> list) {
//     for (T t : list) {
//         System.out.println(t);
//     }
// }
methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "test",
    "(Ljava/util/List;)V",
    // 泛型的签名
    "<T:Ljava/lang/Object;>(Ljava/util/List<TT;>;)V",
    null);
methodVisitor.visitCode();
methodVisitor.visitVarInsn(ALOAD, 1);
methodVisitor.visitMethodInsn(INVOKEINTERFACE, "java/util/List",
    "iterator", "()Ljava/util/Iterator;", true);
methodVisitor.visitVarInsn(ASTORE, 2);
Label label0 = new Label();
methodVisitor.visitLabel(label0);
methodVisitor.visitVarInsn(ALOAD, 2);
methodVisitor.visitMethodInsn(INVOKEINTERFACE, "java/util/Iterator",
    "hasNext", "()Z", true);
Label label1 = new Label();
methodVisitor.visitJumpInsn(IFEQ, label1);
methodVisitor.visitVarInsn(ALOAD, 2);
methodVisitor.visitMethodInsn(INVOKEINTERFACE, "java/util/Iterator",
    "next", "()Ljava/lang/Object;", true);
methodVisitor.visitVarInsn(ASTORE, 3);
methodVisitor.visitFieldInsn(GETSTATIC, "java/lang/System",
    "out", "Ljava/io/PrintStream;");
methodVisitor.visitVarInsn(ALOAD, 3);
methodVisitor.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream",
    "println", "(Ljava/lang/Object;)V", false);
methodVisitor.visitJumpInsn(GOTO, label0);
methodVisitor.visitLabel(label1);
methodVisitor.visitInsn(RETURN);
methodVisitor.visitMaxs(2, 4);
methodVisitor.visitEnd();
```
