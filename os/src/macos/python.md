# Python

```sh
brew install python3
brew install python-tk

# 设置国内镜像源
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip3 config set global.trusted-host pypi.tuna.tsinghua.edu.cn
pip3 config set global.timeout 120

# 移除国内镜像源
pip3 config unset global.index-url
```
