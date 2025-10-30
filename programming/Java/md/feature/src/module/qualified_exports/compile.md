# 编译多模块

手动编译需要按依赖顺序（先编译被依赖的模块）执行命令:

```sh
javac -d out/data.masking \
    src/data.masking/com/example/mask/Mask.java \
    src/data.masking/module-info.java

javac -d out/user.gui \
    --module-path out \
    src/user.gui/com/example/ui/User.java \
    src/user.gui/com/example/ui/Main.java \
    src/user.gui/module-info.java
```

## 运行

```sh
java --module-path out --module user.gui/com.example.ui.Main
```

会出现下面的报错:

```
java.lang.IllegalAccessException: class com.example.mask.Mask (in module data.masking) cannot access class com.example.ui.User (in module user.gui) because module user.gui does not export com.example.ui to module data.masking
	at ...
```

Mask 类中使用了反射获取 User 类的所有字段，这要求 data.masking 模块必须能够访问 user.gui 模块中的 User 类。而访问另一个模块中的类需要满足两个条件:

1. 对目标模块的可读性
2. 目标模块必须导出给定的类

问题是，包含 User 类的包并没有从 user.gui 模块中导出, 所以对于 data.masking 模块来说，User 是不可访问的, 导致了上面的报错。

但是 user.gui 模块不是服务的提供方, 它不应该导出任何的包, 此时就可以使用受限的导出。
