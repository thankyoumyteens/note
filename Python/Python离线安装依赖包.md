# Python离线安装依赖包

要求开发机python版本以及位数必须和离线要安装的主机一致，不然依赖包会出现不匹配的问题

## 打包已安装的包

```
pip list #查看安装的包
pip freeze > requirements.txt
pip download -d packages -r requirements.txt
```

## 离线情况安装打包好的包

将`packages`文件夹和`requirements.txt`拷贝至离线机器上目录下, 
`packages`文件夹放在任意目录下, `requirements.txt`放在同级下
```
pip install --no-index --find-links=packages -r requirements.txt
```
