# grep

基本语法

```sh
grep [选项] "要查找的字符串" [文件或文件夹的路径]
```

常用选项

- `-i` 忽略大小写(不区分大小写搜索)
- `-n` 显示匹配行的行号
- `-v` 反向匹配(排除指定内容)
- `-r` 或 `-R` 递归搜索目录下的所有文件
- `-w` 精确匹配整个单词(避免部分匹配)
- `-E` 使用扩展正则表达式
- `-o` 只显示匹配的内容，而非整行

## 结合管道处理其他命令的输出

```sh
# 查找正在运行的 Python 进程
ps aux | grep "python"
```

## 搜索多个文件

```sh
# 同时在 file1 和 file2 中搜索
grep "pattern" file1.txt file2.txt
```

## 显示匹配行的上下文

- `-A 行数`：显示匹配行及其后面几行的内容
  - 示例 `grep -A 2 "error" log.txt`
- `-B 行数`：显示匹配行及其前面几行的内容
  - 示例 `grep -B 3 "success" log.txt`
- `-C 行数`：显示匹配行及其前后几行的内容, `-C` 可省略
  - 示例`grep -C 2 "warning" log.txt` 或 `grep 2 "warning" log.txt`
