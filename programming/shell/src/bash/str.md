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

## 字符串和算数表达式拼接

```sh
# 使用 $((算数表达式))
echo "1+1=$((1+1))"
```

## 字符串的长度

```sh
str="abc"
echo "str.length=${#str}"
```

## substring

```sh
str="abcdef"
# 从索引1开始截取, 长度为3
sub_str=${str:1:3} # bcd

# cdef
echo "substring=${str:2}"
# def (注意: 空格不能省略)
echo "substring=${str: -3}"

```
