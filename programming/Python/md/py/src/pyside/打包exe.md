# 创建虚拟环境

```sh
# windows
python -m venv packenv
call packenv\scripts\activate.bat
# unix
python3 -m venv packenv
source packenv/bin/activate
```

# 添加依赖库

```
pip install PyInstaller
pip install Pyside6
```

# 打包

```
pyinstaller -w tools_main.py
```

build\和 dist\ 和 pymain.spec 是多出来的打包生成的文件

- build 不需要使用, 可以忽略掉
- dist 路径包含了生的的 exe 和各种依赖文件, 可以直接拿去发布
- pymain.spec 是 pyinstaller 自动生成的配置文件, 后续修改打包配置都可以直接在上面修改

# 打包成单文件

```
pyinstaller -w -F tools_main.py
```

文件变小, 但启动速度变慢

# UPX 压缩

下载 UPX 并解压: [https://github.com/upx/upx/releases](https://github.com/upx/upx/releases)

```
pyinstaller -w -F tools_main.py --upx-dir="C:\upx-4.0.2-win64"
```

# 报错 ModuleNotFoundError: No module named 'xxx'解决

安装依赖

```
pip install xxx
pip install yyy
```

重新打包

```
pyinstaller -w -F tools_main.py --hidden-import xxx --hidden-import yyy
```
