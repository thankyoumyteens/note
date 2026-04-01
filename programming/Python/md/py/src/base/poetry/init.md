# 初始化项目

你可以根据项目是全新的还是已有的，选择不同的初始化方式。

## 创建全新项目

```sh
poetry new my-project
```

这会创建一个名为 my-project 的文件夹，并自动生成标准的目录结构和 pyproject.toml 文件。

## 在现有项目中引入 Poetry

进入你的项目根目录，运行：

```sh
poetry init
```

Poetry 会通过一系列交互式问答（比如项目名称、作者、Python 版本要求等），帮你生成 pyproject.toml 文件。
