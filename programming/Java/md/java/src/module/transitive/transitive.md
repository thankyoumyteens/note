# 传递依赖

假设 api 模块中有一个接口:

```java
public PersonInfo getPersonInfo(String id);
```

其中的 PersonInfo 类在另一个模块: dto 模块中。这样的话, 如果使用者模块包含类似下面的代码:

```java
String name = getPersonInfo("001").getName();
```

就会因为使用者模块无权访问 dto 模块而报错(和 maven 中不同, 无法访问依赖的依赖)。

解决的方法是在 api 模块中, 把对 dto 模块的依赖传递出去, 让依赖 api 模块的模块可以无需显式依赖 dto 模块就能访问 dto 模块导出的包。使用 transitive 关键字来实现依赖的传递。

修改 api 模块的模块描述符:

```java
module api {
    exports com.example.api;
    // 依赖dto模块, 并传递依赖
    requires transitive dto;
}
```

在 requires 后面增加关键字 transitive。表示 api 模块依赖 dto 模块，并且每个导入 api 的模块也会自动依赖 dto 模块。
