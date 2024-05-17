# 获取字段的参数化类型

```java
public class ParameterizedTypeDemo {

    List<String> list = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        Class<ParameterizedTypeDemo> demoClass = ParameterizedTypeDemo.class;
        // 获取字段的参数化类型
        System.out.println(demoClass.getDeclaredField("list").getGenericType());
    }
}
```

运行结果

```
java.util.List<java.lang.String>
```
