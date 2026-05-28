# 创建 python-tools 项目

把 Python 辅助能力从 Java 主工程中隔离出来，避免 Python 脚本散落在项目根目录。

Python 在本路线中是辅助工具，不是主后端。它负责：

```text
eval
批处理
文档处理
接口测试
数据清洗
```

所以放在独立目录：

```text
python-tools/
```

#### 代码

在项目根目录执行：

```bash
mkdir -p python-tools
cd python-tools
uv init --package ai-gateway-tools
```

如果你已经手动创建目录，也可以只创建结构：

```bash
mkdir -p python-tools/src/ai_gateway_tools
mkdir -p python-tools/scripts
touch python-tools/src/ai_gateway_tools/__init__.py
```

#### 代码说明

`uv init` 会创建一个标准 Python 项目结构。uv 官方定位是 Python package/project manager，用来管理项目、依赖和运行命令。
