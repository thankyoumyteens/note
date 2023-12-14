# 变量

Bash 没有数据类型的概念，所有的变量值都是字符串。

## 创建变量

```sh
#声明变量, 等号两边不能有空格
# 变量名=变量值
$ hello="hello world"
```

## 使用变量

```sh
# 读取变量的时候，直接在变量名前加上$就可以了
$ echo $hello
hello world

# 与其它字符串连起来使用时,
# 可以写成可以写成${变量名}
$ file_path="/home/test"
$ echo ${file_path}/hello.txt
/home/test/hello.txt
```
