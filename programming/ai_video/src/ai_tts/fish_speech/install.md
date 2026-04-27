# 搭建 Fish Speech 环境

本文档记录了使用 Docker Compose 快速部署 Fish Speech (含 `s2-pro` 模型) 的完整流程，包括源码获取、模型下载以及多种运行模式的启动命令。

## 📁 一、 准备工作：环境与模型

在启动容器之前，需要先将项目代码克隆到本地，并下载对应的大模型权重文件。

**1. 克隆官方代码仓库**

```bash
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
```

**2. 下载模型权重**
提前通过 Hugging Face 官方工具将 `s2-pro` 模型下载到指定的 `checkpoints` 目录，供 Docker 容器挂载使用。

```bash
# 安装 Hugging Face 命令行工具
pip install huggingface_hub

# 下载 s2-pro 模型到本地 checkpoints/s2-pro 文件夹
huggingface-cli download fishaudio/s2-pro --local-dir checkpoints/s2-pro
```

---

## 🚀 二、 启动核心服务 (已验证成功 ✅)

此部分为主要操作步骤，使用默认的 GPU (CUDA) 环境启动可视化交互界面。

**启动 WebUI 可视化界面**

```bash
docker compose --profile webui up
```

_说明：启动成功后，即可在浏览器中访问 WebUI 进行语音克隆与生成操作。_

---

## 🛠️ 三、 进阶启动模式 (备选)

以下命令适用于特定场景（如需要追求极致推理速度、需要提供接口服务或在无显卡环境运行），可根据后续需求进行尝试：

### 1. 开启编译优化加速 (Compile 模式)

在启动命令前加入 `COMPILE=1` 环境变量，PyTorch 会在底层对算子进行编译融合，以获得更快的推理速度（首次启动加载时间会稍长）。

- **加速启动 WebUI:**
  ```bash
  COMPILE=1 docker compose --profile webui up
  ```
- **加速启动 API 服务:**
  ```bash
  COMPILE=1 docker compose --profile server up
  ```

### 2. 独立 API 服务模式

如果你不需要浏览器可视化界面，而是想通过代码调用（如集成到其他应用中），可单独启动 API Server：

```bash
docker compose --profile server up
```

### 3. 纯 CPU 运行模式

在没有 NVIDIA 显卡或 CUDA 环境的机器上，可以强制使用 CPU 作为计算后端启动服务：

```bash
BACKEND=cpu docker compose --profile webui up
```
