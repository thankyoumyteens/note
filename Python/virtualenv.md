# 安装virtualenv

```
pip install virtualenv
```

# 建立虚拟环境

```
virtualenv –p c:\Python27\Python2.exe d:\Python_virtualenvs\for_django
```
- `-p` 指定你要虚拟的Python版本，这里选择了本地的python2.7
- `–-no-site-packages` 表示在建立虚拟环境时不将原版本中的第三方库拷贝过来，这样就能获得一个纯净的Python环境。virtualenv高版本不再支持。
- `d:\Python_virtualenvs\for_django` 表明在该目录下，建立一个叫做for_django的虚拟环境。

# 使用虚拟环境

windows: 进入要使用的虚拟环境的目录下的script文件夹，运行`activate.bat`

linux: `source 虚拟环境路径/bin/activate`

# 退出虚拟环境

windows: 运行script目录下的`deactivate.bat`

linux: `deactivate`
