# Windows11 + RTX5090Laptop 环境搭建

### 一、 准备基础依赖环境

RTX 5090 属于最新的架构，对驱动和 CUDA 版本的兼容性要求较高。

1.  **更新 NVIDIA 显卡驱动**：
    前往 NVIDIA 官网，下载并安装针对 RTX 5090 Laptop 的最新 Studio 驱动。
2.  **安装 Conda 环境 (Miniconda / Anaconda)**：
    为了更好地隔离和管理 Python 依赖，推荐安装 Miniconda。安装时，建议勾选加入环境变量，或者通过 Anaconda Prompt 来执行后续的命令行操作。
3.  **安装 Git**：
    下载并安装 Git for Windows，用于拉取 ComfyUI 源码和后续安装各种插件。

### 二、 部署 ComfyUI 及 CUDA 环境

打开终端（PowerShell 或 Anaconda Prompt），执行以下步骤：

**1. 克隆 ComfyUI 仓库**

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

**2. 创建并激活虚拟环境**
隔离环境可以避免后续其他 AI 项目（如 LLM 开发）的依赖冲突。

```bash
conda create -n ai_demo python=3.11
conda activate ai_demo
```

_(激活后，命令行提示符前会出现 `(ai_demo)` 标志)_

**3. 安装支持 RTX 5090 的 PyTorch**
RTX 5090 需要较新的 CUDA Toolkit。建议直接安装基于 CUDA 12.1 或 12.4 的 PyTorch 组合：

```bash
# 1. 彻底卸载旧版本（以防文件冲突）
pip uninstall torch torchvision torchaudio xformers -y
# 2. 安装支持 CUDA 13.0 的最新 PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
```

安装完成后，你可以直接在命令行输入 python，然后运行你提供的验证代码来测试 5090 是否被成功识别：

```py
import torch
print(torch.cuda.is_available())
# 如果输出 True，说明显卡驱动和 PyTorch 已经完美打通！
```

**4. 安装 ComfyUI 核心依赖**

```bash
pip install -r requirements.txt
```

### 三、 安装必备管理器与基础模型

由于是全新部署，建议优先安装节点管理器，并准备好基础的生图模型。

**1. 安装 ComfyUI-Manager（强烈推荐）**
这是 ComfyUI 最核心的插件管理器，可以通过它一键安装和更新其他所有节点和模型。

```bash
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..
```

### 四、 针对 RTX 5090 Laptop 的运行优化

RTX 5090 拥有极强的算力和充裕的显存。在本地启动时，可以通过添加启动参数来最大化发挥它的性能。

在 `ComfyUI` 根目录下，创建一个名为 `run.bat` 的批处理文件，填入以下内容：

```bat
call conda activate ai_demo
python main.py
pause
```

双击 `run.bat` 即可启动服务。当控制台提示 `To see the GUI go to: http://127.0.0.1:8188` 时，在浏览器中访问该地址即可开始使用！
