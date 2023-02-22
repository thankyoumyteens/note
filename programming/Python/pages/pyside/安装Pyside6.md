# 安装Pyside6

pip install Pyside6

# Pycharm配置Pyside6

File - Settings - Tools - External Tools 然后点击左上角的加号

## 新增Pyside6-Designer窗口中的填写内容：

- Name: Pyside6-Designer（可自己定义）
- Group: Pyside6（可自己定义）
- Program: C:\Users\walter\AppData\Local\Programs\Python\Python37\Lib\site-packages\PySide6\designer.exe
- Arguments: 空
- Working directory: $FileDir$

点击确定

## 新增Pyside6-UIC窗口中的填写内容：

- Name: Pyside6-UIC（可自己定义）
- Group: Pyside6（可自己定义）
- Program: C:\Users\walter\AppData\Local\Programs\Python\Python37\Scripts\pyside6-uic.exe
- Arguments: $FileName$ -o ui_$FileNameWithoutExtension$.py
- Working directory: $FileDir$

点击确定

## 用法

pycharm主界面，在菜单栏中 Tools - Pyside6 中可以看到新添加的Pyside6-Designer

对使用Pyside6-Designer每次编译保存后的.ui文件右键点击 选择Pyside6 - Pyside6-UIC，运行完成后，会多出一个ui_xxx.py的文件
