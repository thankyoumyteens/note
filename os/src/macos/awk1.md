# 使用自定义分隔符

处理以逗号分隔的文件 csvdata.txt：

```
name,age,job
Alice,25,Engineer
Bob,30,Designer
```

用 `-F` 指定分隔符为逗号，并打印姓名和职业：

```sh
awk -F ',' '{print $1, "的工作是:", $3}' csvdata.txt
```

输出：

```
name 的工作是: job
Alice 的工作是: Engineer
Bob 的工作是: Designer
```
