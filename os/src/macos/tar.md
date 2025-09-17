# tar

常用参数:

- -c: 创建文件
- -C 目录: 指定解压位置
- -x: 解压文件
- -z: 用 gzip 格式压缩或解压
- -f 文件: 要压缩或解压的文件
- -v: 输出执行过程

## 压缩文件

```sh
tar -zcvf demo.tar.gz *.txt *.md
```

## 压缩文件夹, 压缩包内包含文件夹

```sh
tar -zcvf demo.tar.gz dir_path/*.txt dir_path/*.md
# 递归压缩文件夹下所有文件
tar -zcvf demo.tar.gz dir_path/
```

## 压缩文件夹, 压缩包内不包含文件夹

```sh
cd dir_path/
tar -zcvf ../demo.tar.gz *
```

## 列出压缩包内的文件

```sh
tar -tvf demo.tar.gz
```

## 解压

```sh
tar -zxvf demo.tar.gz
```

## 解压到指定文件夹

```sh
tar -zxvf demo.tar.gz -C dist_dir_path/
```
