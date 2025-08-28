# 编译多模块

手动编译需要按依赖顺序（先编译被依赖的模块）执行命令:

```sh
javac -d out/data.transfer.api \
    src/data.transfer.api/com/example/transfer/api/Transfer.java \
    src/data.transfer.api/module-info.java

javac -d out/data.transfer.computer \
    --module-path out \
    src/data.transfer.computer/com/example/device/Computer.java \
    src/data.transfer.computer/module-info.java

javac -d out/user.use \
    --module-path out \
    src/user.use/com/example/use/Main.java \
    src/user.use/module-info.java
```

## 运行

```sh
java --module-path out --module user.use/com.example.use.Main
```
