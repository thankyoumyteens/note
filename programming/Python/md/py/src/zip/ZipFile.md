# ZipFile

## 打开ZIP文件

```py
class zipfile.ZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True)
```
- file 可以是一个文件地址字符串、文件类对象或地址类对象。
- mode 参数为r时, 表示读取一个已经存在的文件；为w的时候表示覆盖或写入一个新文件；为a时表示在已有文件后追加；为x时表示新建文件并写入。x模式下, 如果文件名已经存在, 则抛出FileExistsError异常。
- compression 指明压缩格式
- 当文件大小超过4GB时, 将使用ZIP64扩展（默认启用）。
- 在w/x/a模式下, 如果没有写入任何数据就close了, 则会生成空的ZIP文件。
- ZipFile也是一种上下文管理器, 同样支持with语句

## 关闭ZIP文件

```py
ZipFile.close()
```

## 压缩格式

- `zipfile.ZIP_STORED` 不压缩
- `zipfile.ZIP_DEFLATED` 常用的ZIP压缩方法
- `zipfile.ZIP_BZIP2` BZIP2压缩方法
- `zipfile.ZIP_LZMA` LZMA压缩方法

## 读取zip文档内指定文件

```py
ZipFile.read(filename, pwd=None)
```

- 返回指定文件的二进制数据

## 往ZIP文件里添加新文件

```py
ZipFile.write(filename, arcname=None, compress_type=None)
```
- filename 本地文件路径
- 单个文件可以重复添加, 但是会弹出警告。
- 如果指定arcname参数, 则在ZIP文件内部将原来的filename改成arcname
- compress_type表示压缩格式

## 获取zip文档内文件的信息

- `ZipFile.getinfo(name)` 获取zip文档内指定文件的信息。返回一个zipfile.ZipInfo对象, 它包括文件的详细信息。
- `ZipFile.infolist()` 获取zip文档内所有文件的信息, 返回一个zipfile.ZipInfo的列表。
- `ZipFile.namelist()` 获取zip文档内所有文件的名称列表。

## 压缩文件夹

```py
def zip_dir(source_dir, output_filename, prefix):
    """
    压缩指定文件夹
    :param source_dir: 要压缩的文件夹
    :param output_filename: 压缩文件存放路径
    :param prefix: 压缩文件内的文件夹名
    """
    if os.path.exists(source_dir):
        zipf = zipfile.ZipFile(file=output_filename, mode='w', compression=zipfile.ZIP_DEFLATED)
        pre_len = len(os.path.dirname(source_dir))
        for parent, dir_names, filenames in os.walk(source_dir):
            for filename in filenames:
                absolute_path = os.path.join(parent, filename)
                relative_path = prefix + absolute_path[pre_len:].strip(os.path.sep)
                zipf.write(absolute_path, relative_path)
        zipf.close()
```

## 解压

解压单个文件
```py
ZipFile.extract(member, path=None, pwd=None)
```
解压多个文件
```py
ZipFile.extractall(path=None, members=None, pwd=None)
```

- member 要解压的文件
- members 要解压的文件list 不传是全部解压
- path 指定的解压目录, 默认到当前目录
- pwd 解压密码

```py
import zipfile, os
f = zipfile.ZipFile('duoduo.zip'))  
for file in f.namelist():
　　f.extract(file, r'd:/Work')
f.close()
```
