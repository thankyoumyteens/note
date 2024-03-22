# 分支跳转

test.sh

```sh
if test $1 == "a"; then
    echo "input: a"
elif test $1 == "b"; then
    echo "input: b"
else
    echo "input: other"
fi
```

运行:

```sh
sh ./test.sh a
```

## test 命令

test 命令，有三种形式:

1. `test expression`
2. `[ expression ]`
3. `[[ expression ]]`

第二种和第三种写法，`[`和`]`与内部的表达式之间必须有空格。

`[ ]`是`test`的简写形式, `[[ ]]`提供了字符串比较的更多高级特性, 但不是所有的 shell 都支持双方括号。

## 与

```sh
# if test $1 == "a" && test $2 == "b"; then
if [ $1 == "a" ] && [ $2 == "b" ]; then
    echo "ok"
fi
```

## 或

```sh
if [ $1 == "a" ] || [ $2 == "b" ]; then
    echo "ok"
fi
```

## 非

```sh
if [ $1 != "a" ]; then
    echo "ok"
fi
```
