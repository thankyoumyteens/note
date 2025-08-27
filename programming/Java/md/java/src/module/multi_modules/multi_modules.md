# 多模块应用程序

示例:

- 提供服务的模块: calc.core
- 使用服务的模块: calc.gui

目录结构如下:

```
src
├── calc.core
│   ├── com
│   │   └── example
│   │       └── calc
│   │           └── core
│   │               └── CalcCore.java
│   └── module-info.java
└── calc.gui
    ├── com
    │   └── example
    │       └── calc
    │           └── gui
    │               └── CalcMain.java
    └── module-info.java
```
