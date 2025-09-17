# zip

## 压缩文件

```sh
zip demo.zip *.txt *.md
```

## 压缩文件夹, 压缩包内包含文件夹

```sh
zip demo.zip dir_path/*.txt dir_path/*.md
# 递归压缩文件夹下所有文件
zip -r demo.zip dir_path/
```

## 压缩文件夹, 压缩包内不包含文件夹

```sh
cd dir_path/
zip ../demo.zip *
```

## 列出压缩包内的文件

```sh
unzip -l demo.zip
```

## 解压

```sh
unzip demo.zip
```

## 解压到指定文件夹

```sh
unzip demo.zip -d /home/demo
```
