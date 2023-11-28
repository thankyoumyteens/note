# pathlib

pathlib 是跨平台的、面向对象的路径操作模块, 可适用于不同的操作系统, 其操作对象是各种操作系统中使用的路径（包括绝对路径和相对路径）, pathlib 有两个主要的类, 分别为 PurePath 和 Path。

PurePath 和 Path 最根本的区别在于, PurePath 处理的仅是字符串, 而 Path 则会真正访问底层的文件路径, 因此它提供了属性和方法来访问底层的文件系统。

## pathlib 常用操作

- Path.resolve(): 获得绝对路径
- Path.chmod(): 修改文件权限和时间戳
- Path.mkdir(): 创建目录
- Path.rename(): 重命名文件或文件夹, 如果路径不同, 会移动并重命名
- Path.rmdir(): 删除目录
- Path.unlink(): 删除一个文件
- Path.cwd(): 获得当前工作目录
- Path.exists(): 判断文件或文件夹是否存在
- Path.home(): 返回电脑的用户目录
- Path.is_dir(): 判断路径是不是文件夹
- Path.is_file(): 判断路径是不是文件
- Path.stat(): 获得文件属性
- Path.samefile(): 判断两个路径是否相同
- PurePath.is_absolute(): 判断是否为绝对路径
- PurePath.joinpath(): 拼接路径
- PurePath.name(): 返回文件名
- PurePath.parent(): 返回文件路径
- PurePath.suffix(): 分离文件名和扩展名

```python
from pathlib import Path

source_dir = Path(source_dir)
print(source_dir.is_dir())
```
