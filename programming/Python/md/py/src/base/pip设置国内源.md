# pip 设置国内源

- 清华大学：https://pypi.tuna.tsinghua.edu.cn/simple
- 阿里云：http://mirrors.aliyun.com/pypi/simple
- 豆瓣：http://pypi.douban.com/simple
- 中科大：https://pypi.mirrors.ustc.edu.cn/simple
- 网易： https://mirrors.163.com/pypi/simple
- 华为：https://repo.huaweicloud.com/repository/pypi/simple
- 腾讯：https://mirrors.cloud.tencent.com/pypi/simple

## 通过命令生成配置文件

```sh
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
pip config set global.timeout 120
```

## 安装时临时指定

```sh
pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple
```
