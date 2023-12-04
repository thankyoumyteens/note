# 通配符

## ~

波浪线 ~ 代表当前用户的主目录:

```sh
# 输出当前用户的主目录
echo ~
# 切换到主目录下的dir1目录
cd ~/dir1
# 输出root用户的主目录
echo ~root
```

## ?

?代表文件路径里面的任意单个字符，不包括空字符:

```sh
$ touch test001.txt
$ ls test???.txt
test001.txt
$ ls test?.txt
ls: cannot access 'test?.txt': No such file or directory
```

## \*

\*代表文件路径里面的任意多个字符:

```sh
$ touch test001.txt
$ touch test002.txt
$ ls test*.txt
test001.txt  test002.txt
```

\*只匹配当前目录，不会匹配子目录

```sh
$ mkdir dir1
$ touch test001.txt
$ touch dir1/test001.txt
# 不会匹配子目录
$ ls test*.txt
test001.txt
# 匹配一层子目录
$ ls */test*.txt
dir1/test001.txt
```

## \[\]

\[\]与正则表达式的\[\]一样:

```sh
$ touch a.txt b.txt c.txt
$ ls [ab].txt
a.txt  b.txt
$ ls [!ab].txt
c.txt
$ ls [a-z].txt
a.txt  b.txt  c.txt
$ ls [!a-z].txt
ls: cannot access '[!a-z].txt': No such file or directory
```

## {}

{}会把大括号里面的所有值列出来, 各个值之间使用逗号分隔:

```sh
$ echo {a,b,c}.txt
a.txt b.txt c.txt

$ echo {a..c}.txt
a.txt b.txt c.txt

$ touch a.txt b.txt c.txt
$ ls {a..d}.txt
ls: cannot access 'd.txt': No such file or directory
a.txt  b.txt  c.txt
```

## \$

\$开头的字符串会被作为为变量:

```sh
$ echo $PATH
/usr/local/bin:/usr/bin:...

# ${}也可以表示变量
$ echo ${PATH}
/usr/local/bin:/usr/bin:...
```

## \$()

\$()会返回另一个命令的运行结果:

```sh
$ echo $(date)
Mon Dec 4 19:01:00 CST 2023
```

## \$(())

\$(())会返回算术表达式的运行结果:

```sh
$ echo $((1+1))
2
```
