# awk

基本语法

```sh
awk [选项] '模式 { 动作 }' 文件名
```

- 模式: 用于匹配输入行的条件，这个可选
- 动作: 在匹配到 pattern 时执行的操作
- 文件名: 要处理的文件名

awk 会把每行文本都按分隔符(默认是空格)分成多列, 然后执行 `动作`。

## 基本使用

假设 demo.txt 的内容如下:

```
Alice 25 Engineer
Bob 30 Designer
Charlie 35 Manager
```

使用 awk 打印每个人的姓名（第 1 列）和年龄（第 2 列）：

```sh
awk '{print $1, $2}' ./demo.txt
```

输出:

```
Alice 25
Bob 30
Charlie 35
```
