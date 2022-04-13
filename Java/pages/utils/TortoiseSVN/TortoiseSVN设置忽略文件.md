右键->TortoiseSVN->设置->常规设置->Subversion配置文件:->编辑按钮

编辑global-ignores属性，注意取消前面的注释

```conf
global-ignores = *.iml .idea .idea/* *.class target target/* node_modules node_modules/* .vscode .vscode/* *.o *.lo *.la *.al .libs *.so *.so.[0-9]* *.a *.pyc *.pyo __pycache__
```
保存文件
