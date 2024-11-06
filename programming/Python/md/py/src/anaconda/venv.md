# 虚拟环境

1. 列出可安装的 Python 版本

```sh
conda search python
```

2. 创建指定 Python 版本的环境

```sh
conda create -n demo_env python=3.10
```

3. 进入虚拟环境

```sh
conda activate demo_env
```

4. 退出当前环境

```sh
conda deactivate
```

5. 列出所有环境

```sh
conda env list
```

6. 删除环境

```sh
conda env remove -n demo_env
```
