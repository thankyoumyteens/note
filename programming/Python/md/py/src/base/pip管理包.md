# pip 管理包

```sh
pip install 包名
```

## 指定版本号

```sh
pip install 包名 == 版本号
```

- `==` 指定版本号
- `=>` 高于此版本号
- `<=` 小于此版本号
- `<` 小于此版本号
- `>` 大于此版本号

## 生成 requirements.txt

```sh
pip freeze > requirements.txt
```

## 安装 requirements.txt

```sh
pip install -r requirements.txt
```
