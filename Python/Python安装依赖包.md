# Python安装依赖包

requirements.txt 用来记录项目所有的依赖包和版本号，只需要一个简单的 pip 命令就能生成requirements.txt
```
pip freeze > requirements.txt
```
然后就可以安装依赖
```
pip install -r requirements.txt
```
