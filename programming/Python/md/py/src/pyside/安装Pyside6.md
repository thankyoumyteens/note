# 安装 Pyside6

pip install Pyside6

# Pycharm 配置 Pyside6

File - Settings - Tools - External Tools 然后点击左上角的加号

## 新增 Pyside6-Designer 窗口中的填写内容:

- Name: Pyside6-Designer（可自己定义）
- Group: Pyside6（可自己定义）
- Program: C:\Users\walter\AppData\Local\Programs\Python\Python37\Lib\site-packages\PySide6\designer.exe
- Arguments: 空
- Working directory: $FileDir$

点击确定

## 新增 Pyside6-UIC 窗口中的填写内容:

- Name: Pyside6-UIC（可自己定义）
- Group: Pyside6（可自己定义）
- Program: C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-uic.exe
- Arguments: $FileName$ -o ui\_$FileNameWithoutExtension$.py
- Working directory: $FileDir$

点击确定

## 用法

pycharm 主界面, 在菜单栏中 Tools - Pyside6 中可以看到新添加的 Pyside6-Designer

对使用 Pyside6-Designer 每次编译保存后的.ui 文件右键点击 选择 Pyside6 - Pyside6-UIC, 运行完成后, 会多出一个 ui_xxx.py 的文件

# VS Code 配置 Pyside6

Python 扩展: seanwu.vscode-qt-for-python

打开设置, 搜索: @ext:seanwu.vscode-qt-for-python

在 Designer: Path 项下填写 qt desiner 的路径:
C:\Users\walter\AppData\Local\Programs\Python\Python37\Lib\site-packages\PySide6\designer.exe

在 Rcc: Path 项下填写 pyside6-rcc 的路径:
C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-rcc.exe

在 Uic: Path 项下填写 pyside6-uic 的路径:
C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-uic.exe

## 用法

- 创建.ui 文件: 文件夹上右键 -> Create Qt UI File (designer)
- 编辑.ui 文件: 文件上右键 -> Edit Qt UI File (designer)
- .ui 文件保存后会自动转换为 xxx_ui.py 文件
- 手动转换.ui 文件: 文件上右键 -> Compile Qt UI File (uic)
