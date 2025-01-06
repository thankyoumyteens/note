# 安装

pip install Pyside6

## Pycharm 配置 Pyside6

左上角 PyCharm - Settings - Tools - External Tools 然后点击左上角的加号

### 新增 Pyside6-Designer

- Name: `Pyside6-Designer`
- Group: `Pyside6`
- Program: `/python虚拟环境路径/lib/python3.12/site-packages/PySide6/Designer.app/Contents/MacOS/Designer`
- Arguments: 空
- Working directory: `$FileDir$`

### 新增 Pyside6-UIC

- Name: `Pyside6-UIC`
- Group: `Pyside6`
- Program: `/python虚拟环境路径/bin/pyside6-uic`
- Arguments: `$FileName$ -o ui_$FileNameWithoutExtension$.py`
- Working directory: `$FileDir$`

## 用法

pycharm 主界面，在菜单栏中 Tools - Pyside6 中可以看到新添加的 Pyside6-Designer

对使用 Pyside6-Designer 每次编译保存后的 .ui 文件右键点击 选择 Pyside6 - Pyside6-UIC，运行完成后，会多出一个 ui_xxx.py 的文件
