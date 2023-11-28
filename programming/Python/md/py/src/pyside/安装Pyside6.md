# 安装Pyside6

pip install Pyside6

# Pycharm配置Pyside6

File - Settings - Tools - External Tools 然后点击左上角的加号

## 新增Pyside6-Designer窗口中的填写内容: 

- Name: Pyside6-Designer（可自己定义）
- Group: Pyside6（可自己定义）
- Program: C:\Users\walter\AppData\Local\Programs\Python\Python37\Lib\site-packages\PySide6\designer.exe
- Arguments: 空
- Working directory: $FileDir$

点击确定

## 新增Pyside6-UIC窗口中的填写内容: 

- Name: Pyside6-UIC（可自己定义）
- Group: Pyside6（可自己定义）
- Program: C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-uic.exe
- Arguments: $FileName$ -o ui_$FileNameWithoutExtension$.py
- Working directory: $FileDir$

点击确定

## 用法

pycharm主界面, 在菜单栏中 Tools - Pyside6 中可以看到新添加的Pyside6-Designer

对使用Pyside6-Designer每次编译保存后的.ui文件右键点击 选择Pyside6 - Pyside6-UIC, 运行完成后, 会多出一个ui_xxx.py的文件

# VS Code配置Pyside6

Python扩展: seanwu.vscode-qt-for-python

打开设置, 搜索: @ext:seanwu.vscode-qt-for-python

在Designer: Path 项下填写qt desiner的路径:
C:\Users\walter\AppData\Local\Programs\Python\Python37\Lib\site-packages\PySide6\designer.exe

在Rcc: Path 项下填写pyside6-rcc的路径:
C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-rcc.exe

在Uic: Path 项下填写pyside6-uic的路径:
C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-uic.exe

## 用法

- 创建.ui文件: 文件夹上右键 -> Create Qt UI File (designer)
- 编辑.ui文件: 文件上右键 -> Edit Qt UI File (designer)
- .ui文件保存后会自动转换为xxx_ui.py文件
- 手动转换.ui文件: 文件上右键 -> Compile Qt UI File (uic)
