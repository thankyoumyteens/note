# 7z

## 压缩文件

```sh
# 一般格式(压缩格式为7z)
7zz a demo.7z *.txt
# 指定格式压缩(-t可选值: zip、7z、gzip、bzip2、tar等)
7zz a -t7z demo.7z *.txt
# 指定压缩等级(-mx可选值: 0到9, 0表示不压缩)
7zz a -t7z demo.7z *.txt -mx9
```

## 压缩文件夹, 压缩包内包含文件夹

```sh
7zz a demo.7z demo_dir/
```

## 压缩文件夹, 压缩包内不包含文件夹

```sh
7zz a demo.7z demo_dir/*
```

## 列出压缩包内的文件

```sh
# 小写的L
7zz l demo.7z
```

## 解压

```sh
# 去掉最外层文件夹
7zz e demo.7z
# 保留最外层文件夹(保持原状)
7zz x demo.7z
```

## 解压到指定文件夹

```sh
# -o和文件夹名需要连在一起
7zz x demo.7z -odemo_dir_new/
```
