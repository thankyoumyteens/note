# Python离线安装依赖包(要求两边python版本一致)
打包已安装的包
```
pip freeze > requirements.txt
pip download -d packages -r requirements.txt
```
将packages文件夹和requirements.txt拷贝至离线机器上相同目录下
```
pip install --no-index --find-links=packages -r requirements.txt
```
