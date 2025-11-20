# 虚拟环境操作

## 列出可安装的 Python 版本

```sh
conda search python
```

## 列出所有环境

```sh
conda env list
```

## 创建指定 Python 版本的环境

```sh
conda create -n demo_env python=3.10
```

创建虚拟环境时，可以直接指定要安装的库:

```sh
conda create -n myenv python=3.9 numpy pandas=1.5.0
```

## 进入虚拟环境

```sh
conda activate demo_env
```

## 退出当前环境

```sh
conda deactivate
```

## 删除指定环境

```sh
conda env remove -n demo_env
```
