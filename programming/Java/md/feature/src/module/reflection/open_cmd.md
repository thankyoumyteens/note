# 使用命令行选项开放

有时需要对第三方模块(无法修改源码)进行反射。在这种情况下, 可以使用 java 命令的命令行选项:

```sh
--add-opens 模块/包=目标模块
```

比如

```sh
java --add-opens mymodule1/com.example.demo=module2
```
