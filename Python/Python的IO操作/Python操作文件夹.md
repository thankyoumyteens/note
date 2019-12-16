# Python创建文件夹

1. `os.makedirs(path)` 多层创建目录
2. `os.mkdir(path)` 创建目录

# Python删除文件夹

1. `os.rmdirs(path)` 删除多层目录, 只能删除空文件夹, 删除非空文件夹会报错
2. `os.rmdir(path)` 删除目录, 只能删除空文件夹, 删除非空文件夹会报错
3. `shutil.rmtree(path)` 可以删除非空文件夹
