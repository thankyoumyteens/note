# 编译多模块

```sh
javac -d out --module-source-path src --module calc.gui
```

`--module-source-path` 告诉 javac 在编译期间去哪里查找源格式的其他模块。在多模块模式下进行编译时，必须使用 `-d` 提供目标目录。编译之后，目标目录包含了分解模块格式的编译模块。此输出目录还可以用作运行模块时模块路径上的一个元素。

由于所有模块是被编译在一起的。只需使用 `--module` 指定要编译的实际模块即可，而无须列出所有源文件作为编译器的输入。在这种情况下，提供 `calc.gui` 模块就足够了。编译器通过模块描述符知道，`calc.gui` 依赖 `calc.core` (也是通过模块源路径进行编译)。

```
out
├── calc.core
│   ├── com
│   │   └── example
│   │       └── calc
│   │           └── core
│   │               └── CalcCore.class
│   └── module-info.class
└── calc.gui
    ├── com
    │   └── example
    │       └── calc
    │           └── gui
    │               └── CalcMain.class
    └── module-info.class
```

## 运行

```sh
java --module-path out --module calc.gui/com.example.calc.gui.CalcMain
```
