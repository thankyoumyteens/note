# JShell

JShell 是 Java 9 引入的交互式编程工具（REPL，Read-Eval-Print Loop），允许开发者在命令行中实时输入、执行 Java 代码片段，并即时获得即时反馈，无需编写完整类或方法，极大简化了代码测试、学习和原型验证流程。

## 启动

确保安装 JDK 9+，在命令行输入 `jshell` 即可进入交互环境。

```sh
# 表达式
jshell> 1 + 2
$1 ==> 3

# 变量定义
jshell> String name = "JShell"
name ==> "JShell"

# 调用方法
jshell> name.length()
$3 ==> 6
```

注意: 未命名的结果会自动生成临时变量（如 `$1`、`$3`），可直接复用。

## 退出

输入 `exit` 或 `/exit` 并回车。
