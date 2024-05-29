# 获取方法的参数化类型

```java
public class ParameterizedTypeDemo {

    public void test(List<Integer> list) {
        System.out.println(list);
    }

    public static void main(String[] args) throws Exception {
        Class<ParameterizedTypeDemo> demoClass = ParameterizedTypeDemo.class;
        /*
         * 获取方法参数的参数化类型
         */
        Method test = demoClass.getDeclaredMethod("test", List.class);
        // 获取方法的所有参数
        Type[] types = test.getGenericParameterTypes();
        for (Type type : types) {
            // 判断方法参数是否是泛型
            if (type instanceof ParameterizedType) {
                // 取出泛型参数中所有的泛型
                ParameterizedType pt = (ParameterizedType) type;
                Type[] arguments = pt.getActualTypeArguments();
                for (Type paramType : arguments) {
                    System.out.println(paramType);
                }
            }
        }
    }
}
```

运行结果

```
class java.lang.Integer
```
