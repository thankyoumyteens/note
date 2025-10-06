# 通过 TypeReference 获取泛型信息

在 Java 中，`TypeReference` 是 Jackson、Fastjson 等 JSON 框架中常用的工具类，主要用于解决泛型类型擦除(Type Erasure)问题，以便在运行时获取泛型的具体类型信息。其核心原理是利用**匿名内部类在编译时保留泛型参数信息**的特性，并通过反射机制提取这些信息。

## 核心原理

在 Java 中，无法直接通过反射获取当前类自身的泛型参数（如 `class MyClass<T>` 中 T 的具体类型），核心原因是 Java 的泛型擦除机制(编译后仅保留原始类型)，以及泛型参数信息在编译后的存储方式限制。

虽然泛型参数在类自身定义中会被擦除，但 Java 会在泛型被具体使用的地方保留部分泛型信息(存储在类的字节码的 “签名” 中)，例如：

- 子类继承泛型父类时，若指定了具体泛型参数（如 `class SubClass extends MyClass<String>`），则 SubClass 的字节码会保留 `MyClass<String>` 的信息
- 匿名内部类指定泛型参数时(如 `new TypeReference<List<String>>(){}`)，匿名类的字节码会保留 `List<String>` 的信息

这些被保留的泛型信息可以通过反射获取(如 `getGenericSuperclass()`)，但类自身定义的泛型参数(如 `MyClass<T>` 中的 T)不会被保留，因为它是 “未绑定” 的类型变量，而非具体类型。

## 通过 TypeReference 获取泛型信息

以 Jackson 框架的 `com.fasterxml.jackson.core.type.TypeReference` 为例，步骤如下：

### 1. 定义 TypeReference 匿名实例并指定泛型

通过匿名内部类继承 `TypeReference`，并在继承时明确泛型参数(如 `List<String>`、`Map<Integer, User>` 等)。此时，泛型信息会被保留在类的元数据中。

```java
import com.fasterxml.jackson.core.type.TypeReference;
import java.util.List;
import java.util.Map;

// 示例1：获取 List<String> 的泛型信息
TypeReference<List<String>> listTypeRef = new TypeReference<List<String>>() {};

// 示例2：获取 Map<Integer, User> 的泛型信息
TypeReference<Map<Integer, User>> mapTypeRef = new TypeReference<Map<Integer, User>>() {};
```

### 2. 通过 TypeReference 的方法获取泛型类型

`TypeReference` 通常提供 `getType()` 方法，返回一个 `Type` 对象，该对象包含了完整的泛型信息。通过解析 `Type` 对象，可提取泛型的具体参数。

```java
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;

// 获取 Type 对象（包含泛型信息）
Type type = listTypeRef.getType();

// 判断是否为参数化类型（带泛型的类型）
if (type instanceof ParameterizedType) {
    ParameterizedType parameterizedType = (ParameterizedType) type;

    // 获取原始类型（如 List）
    Type rawType = parameterizedType.getRawType();
    System.out.println("原始类型：" + rawType); // 输出：interface java.util.List

    // 获取泛型参数（如 String）
    Type[] actualTypeArguments = parameterizedType.getActualTypeArguments();
    for (Type arg : actualTypeArguments) {
        System.out.println("泛型参数：" + arg); // 输出：class java.lang.String
    }
}
```

### 3. 复杂泛型的解析（嵌套泛型）

对于嵌套泛型（如 `List<Map<String, Integer>>`），可递归解析 `ParameterizedType`：

```java
// 定义嵌套泛型的 TypeReference
TypeReference<List<Map<String, Integer>>> nestedTypeRef = new TypeReference<List<Map<String, Integer>>>() {};

Type nestedType = nestedTypeRef.getType();
if (nestedType instanceof ParameterizedType) {
    ParameterizedType outerType = (ParameterizedType) nestedType;
    System.out.println("外层原始类型：" + outerType.getRawType()); // List

    // 解析外层泛型参数（Map<String, Integer>）
    Type innerType = outerType.getActualTypeArguments()[0];
    if (innerType instanceof ParameterizedType) {
        ParameterizedType innerParamType = (ParameterizedType) innerType;
        System.out.println("内层原始类型：" + innerParamType.getRawType()); // Map
        System.out.println("内层泛型参数1：" + innerParamType.getActualTypeArguments()[0]); // String
        System.out.println("内层泛型参数2：" + innerParamType.getActualTypeArguments()[1]); // Integer
    }
}
```

## 自己实现 TypeReference

如果不依赖第三方框架，也可以自己实现一个简单的 `TypeReference`，核心是通过反射获取父类的泛型参数:

```java
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;

public abstract class MyTypeReference<T> {
    private final Type type;

    public MyTypeReference() {
        // 获取父类（即 MyTypeReference<T>）的泛型信息
        Type superClass = getClass().getGenericSuperclass();
        // 强转为参数化类型（带泛型的父类）
        this.type = ((ParameterizedType) superClass).getActualTypeArguments()[0];
    }

    public Type getType() {
        return type;
    }
}

// 使用自定义 TypeReference
public class Test {
    public static void main(String[] args) {
        MyTypeReference<List<String>> ref = new MyTypeReference<List<String>>() {};
        Type type = ref.getType();
        System.out.println(type); // 输出：java.util.List<java.lang.String>
    }
}
```
