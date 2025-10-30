# 打包和运行

### 1. 打包

在项目根目录执行以下命令，编译并打包所有模块：

```bash
mvn clean package
```

打包后，每个模块的 `target` 目录下会生成模块化 JAR：

- `calculator/target/calculator-1.0.0.jar`
- `calculator-impl/target/calculator-impl-1.0.0.jar`
- `ui/target/ui-1.0.0.jar`

### 2. 运行程序

通过 `java` 命令的 `--module-path` 指定模块路径，`--module` 指定主模块和主类：

```sh
java --module-path "calculator/target/calculator-1.0-SNAPSHOT.jar:calculator-impl/target/calculator-impl-1.0-SNAPSHOT.jar:ui/target/ui-1.0-SNAPSHOT.jar" \
     --module calculator.ui/com.example.App
```
