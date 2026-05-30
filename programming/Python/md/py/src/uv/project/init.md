# 初始化项目

## 1. 在新目录初始化项目

```sh
uv init my-project
cd my-project
```

一般会生成类似这些文件：

```
my-project/
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

## 2. 在当前目录初始化

如果你已经建好了目录：

```sh
mkdir my-project
cd my-project
uv init
```

## 3. 使用指定 Python 版本初始化项目

```sh
uv init --python 3.12 my-project
```
