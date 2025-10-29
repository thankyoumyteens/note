# 接口的默认实现

接口修改后，实现它的类也必须跟着改。为了解决这个问题, 从 Java8 开始, 接口中的方法可以用 `default` 或 `static` 修饰，这样就可以有方法体，实现类也不必重写此方法。

- default 修饰的方法，是普通实例方法，可以用 this 调用，可以被子类继承、重写
- static 修饰的方法，使用上和一般类静态方法一样。但它不能被子类继承，只能用 `接口.方法()` 的形式调用

```java
public interface ConnectionFactory {
    default Connection getConnection() {
        return new DefaultConnection();
    }
}
```
