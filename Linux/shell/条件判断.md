# 语法

```sh
if [ command ];then
符合该条件执行的语句
elif [ command ];then
符合该条件执行的语句
else
符合该条件执行的语句
fi
```

- 如果command执行后返回0，则表示true
- `[ ]`表示条件测试。注意这里的空格很重要。要注意在`[`后面和`]`前面都必须要有空格
- 注意if判断中对于变量的处理，需要加引号，以免一些不必要的错误。如`if [ ! -f "$doiido" ]; then`

# command

## 文件/目录判断

- `-a FILE` 如果 FILE 存在则为真。
- `-b FILE` 如果 FILE 存在且是一个块文件则返回为真。
- `-c FILE` 如果 FILE 存在且是一个字符文件则返回为真。
- `-d FILE` 如果 FILE 存在且是一个目录则返回为真。
- `-e FILE` 如果 指定的文件或目录存在时返回为真。
- `-f FILE` 如果 FILE 存在且是一个普通文件则返回为真。
- `-g FILE` 如果 FILE 存在且设置了SGID则返回为真。
- `-h FILE` 如果 FILE 存在且是一个符号符号链接文件则返回为真。（该选项在一些老系统上无效）
- `-k FILE` 如果 FILE 存在且已经设置了冒险位则返回为真。
- `-p FILE` 如果 FILE 存并且是命令管道时返回为真。
- `-r FILE` 如果 FILE 存在且是可读的则返回为真。
- `-s FILE` 如果 FILE 存在且大小非0时为真则返回为真。
- `-u FILE` 如果 FILE 存在且设置了SUID位时返回为真。
- `-w FILE` 如果 FILE 存在且是可写的则返回为真。（一个目录为了它的内容被访问必然是可执行的）
- `-x FILE` 如果 FILE 存在且是可执行的则返回为真。
- `-O FILE` 如果 FILE 存在且属有效用户ID则返回为真。
- `-G FILE` 如果 FILE 存在且默认组为当前组则返回为真。（只检查系统默认组）
- `-L FILE` 如果 FILE 存在且是一个符号连接则返回为真。
- `-N FILE` 如果 FILE 存在 and has been mod如果ied since it was last read则返回为真。
- `-S FILE` 如果 FILE 存在且是一个套接字则返回为真。
- `FILE1 -nt FILE2` 如果 FILE1 比 FILE2 新, 或者 FILE1 存在但是 FILE2 不存在则返回为真。
- `FILE1 -ot FILE2` 如果 FILE1 比 FILE2 老, 或者 FILE2 存在但是 FILE1 不存在则返回为真。
- `FILE1 -ef FILE2` 如果 FILE1 和 FILE2 指向相同的设备和节点号则返回为真。

## 字符串判断

- `-z STRING` 如果STRING为空是真
- `-n STRING` 如果STRING非空是真
- `STRING1`　 如果字符串不为空则返回为真,与-n类似
- `STRING1 == STRING2` 如果两个字符串相同则返回为真
- `STRING1 != STRING2` 如果字符串不相同则返回为真
- `STRING1 < STRING2` 如果 “STRING1”字典排序在“STRING2”前面则返回为真。
- `STRING1 > STRING2` 如果 “STRING1”字典排序在“STRING2”后面则返回为真。

# 数值判断

- `INT1 -eq INT2` INT1和INT2两数相等返回为真
- `INT1 -ne INT2` INT1和INT2两数不等返回为真
- `INT1 -gt INT2` INT1大于INT2返回为真
- `INT1 -ge INT2` INT1大于等于INT2返回为真
- `INT1 -lt INT2` INT1小于INT2返回为真
- `INT1 -le INT2` INT1小于等于INT2返回为真

# 逻辑判断

- `! EXPR` 逻辑非，如果 EXPR 是false则返回为真。
- `EXPR1 -a EXPR2` 逻辑与，如果 EXPR1 and EXPR2 全真则返回为真。
- `EXPR1 -o EXPR2` 逻辑或，如果 EXPR1 或者 EXPR2 为真则返回为真。
- `[ ] || [ ]` 用OR来合并两个条件
- `[ ] && [ ]` 用AND来合并两个条件
