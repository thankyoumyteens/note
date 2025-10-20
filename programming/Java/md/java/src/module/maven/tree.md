# 创建项目

目录结构如下：

```
.
├── calculator
│   ├── pom.xml
│   └── src
│       └── main
│           └── java
│               ├── com
│               │   └── example
│               │       └── api
│               │           └── Calculate.java
│               └── module-info.java
├── calculator-impl
│   ├── pom.xml
│   └── src
│       └── main
│           └── java
│               ├── com
│               │   └── example
│               │       └── impl
│               │           └── SimpleCalculator.java
│               └── module-info.java
├── pom.xml
└── ui
    ├── pom.xml
    └── src
        └── main
            └── java
                ├── com
                │   └── example
                │       └── App.java
                └── module-info.java
```

- **`calculator`**：API 模块（提供接口 `Calculate`），无依赖
- **`calculator-impl`**：实现模块（实现 `Calculate` 接口），依赖 `calculator`
- **`ui`**：主程序模块（调用实现类），依赖 `calculator-impl`
