# 字符串操作

## 字符串和变量拼接

```sh
val="ok"
# 使用 ${变量名}
echo "ok=${ok}"
```

## 字符串和命令拼接

```sh
# 使用 $(命令), 并不是所有的类unix系统都支持这种方式
echo "os version=$(uname -a)"
# 或者使用 `命令`
echo "os version=`uname -a`"
```
