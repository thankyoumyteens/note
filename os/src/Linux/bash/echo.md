# echo 命令

echo 命令的作用是在屏幕输出一行文本:

```sh
$ echo ok
ok
```

输出多行文本, 需要把多行文本放在引号里面:

```sh
$ echo "
      line 1
      line 2
"

      line 1
      line 2
```

## 取消末尾的回车符

默认情况下，echo 输出的文本末尾会有一个回车符。-n 参数可以取消末尾的回车符，使得下一个提示符紧跟在输出内容的后面:

```sh
$ echo -n ok
ok$
```

## 解析特殊字符

默认情况下，echo 不解释特殊字符，原样输出。-e 参数会解释引号里面的特殊字符:

```sh
$ echo "line1\nline2"
line1\nline2

$ echo -e "line1\nline2"
line1
line2
```
