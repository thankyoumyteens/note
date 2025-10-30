# 受限的导出

在某些情况下，可能只需要将包暴露给特定的某些模块。此时，可以在模块描述符中使用收限制的导出。

示例:

- 提供功能的模块: data.masking
- 使用功能的模块: user.gui

目录结构如下:

```
src
├── data.masking
│   ├── com
│   │   └── example
│   │       └── mask
│   │           └── Mask.java
│   └── module-info.java
└── user.gui
    ├── com
    │   └── example
    │       └── ui
    │           ├── Main.java
    │           └── User.java
    └── module-info.java
```
