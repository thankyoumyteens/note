# 服务

如果编写以下代码:

```java
MyInterface i = new MyImpl();
```

使用接口的某个实现类时，就必须导出这个具体的实现类。因此，功能的使用者和功能的提供者之间存在强耦合。这样一来，实现类的任何更改都会直接影响到所有的使用者。

许多 Java 应用程序使用了依赖注入(Dependency Injection, DI)来实现对接口进行编程，同时与实现类松耦合。DI 负责根据注解或 XML 给应用程序注入实现类的对象。这通常被称为控制反转(Inversion of Control, IoC), 因为框架控制了类的实例化, 而不是应用程序本身。

服务(service)通过另外的方式(而不是通过依赖注入)提供了 IoC。

使用服务的步骤:

1. 定义接口
2. 接口的实现类所在的模块通过 `provides 接口的全类名 with 实现类的全类名;` 声明该模块提供了服务
3. 功能的使用者模块通过 `uses 接口的全类名;` 告诉 java 模块系统它需要使用这个接口的实现类, 该模块本身无需导入实现类所在的模块
4. 功能的使用者通过 `ServiceLoader.load(接口类.class);` 获取这个接口当前所有可用的实现类的对象

示例:

- 接口模块: data.transfer.api
- 实现类模块: data.transfer.computer
- 使用者模块: user.use

```
src
├── data.transfer.api
│   ├── com
│   │   └── example
│   │       └── transfer
│   │           └── api
│   │               └── Transfer.java
│   └── module-info.java
├── data.transfer.computer
│   ├── com
│   │   └── example
│   │       └── device
│   │           └── Computer.java
│   └── module-info.java
└── user.use
    ├── com
    │   └── example
    │       └── use
    │           └── Main.java
    └── module-info.java
```
