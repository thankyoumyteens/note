# 搭建 Fish Speech 环境

## 🖥️ 一、 系统要求与环境准备

- **操作系统**：Linux 或 Windows 的 WSL2（官方明确提示：编译加速不支持 Windows 原生环境）。
- **硬件要求**：建议至少 24GB 显存的 GPU（用于推理 s2-pro 等大模型）。
- **前置依赖**：
  - 已安装 Docker 和 Docker Compose。
  - **关键**：已安装 `NVIDIA Docker runtime`（在 WSL2 下使用 Docker Desktop 会自带该支持，无需额外折腾）。

## 📁 二、 获取代码与模型权重

容器启动前，必须将代码和模型准备好，因为 Docker 会默认读取本地映射的目录。

**1. 克隆官方代码仓库**

```bash
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
```

**2. 下载核心模型权重**
提前通过 Hugging Face 官方工具将 `s2-pro` 模型下载到指定的 `checkpoints` 目录。

```bash
# 安装下载工具
pip install huggingface_hub

# 强制下载到本地的 checkpoints/s2-pro 目录
huggingface-cli download fishaudio/s2-pro --local-dir checkpoints/s2-pro
```

## 📂 三、 目录挂载规范 (必读)

为了让 Docker 容器能读取到你的文件，项目默认设定了两个核心的“数据通道”（卷挂载）。你在使用时，请将文件放入对应文件夹：

- `./checkpoints` ➡️ 映射到容器的 `/app/checkpoints`（**存放下载好的大模型，如 s2-pro**）。
- `./references` ➡️ 映射到容器的 `/app/references`（**存放你准备好的参考音频，比如守岸人的 wav 文件**，方便在 WebUI 中直接调用）。

## 🚀 四、 启动服务 (基础模式)

确保你在 `fish-speech` 目录下，根据你的需求选择以下命令：

**1. 启动 WebUI (可视化界面)** —— _日常克隆语音推荐_

```bash
docker compose --profile webui up
```

_启动后浏览器访问：`http://localhost:7860`_

**2. 启动 API Server (接口服务)** —— _代码调用/二次开发推荐_

```bash
docker compose --profile server up
```

_启动后 API 访问：`http://localhost:8080`_

**3. 仅 CPU 运行模式** —— _无显卡环境备用_

```bash
BACKEND=cpu docker compose --profile webui up
```

## ⚡ 五、 进阶：性能全开模式 (Compile)

官方文档指出，启用 `torch.compile` 可以使 **推理速度提升约 10 倍**！（这也是为什么我们必须用 Linux/WSL2 的原因，Windows 无法使用此特性）。

**启用 10x 加速启动 WebUI：**

```bash
COMPILE=1 docker compose --profile webui up
```

**启用 10x 加速启动 API Server：**

```bash
COMPILE=1 docker compose --profile server up
```

_(注：开启 `COMPILE=1` 后，首次生成语音时由于底层需要实时编译 CUDA 算子，等待时间会比较长，但从第二次开始速度将极其恐怖。)_

## ⚙️ 六、 自定义端口与环境变量设置

如果你不想每次都在命令行里敲环境变量，或者 `7860` 端口被占用了，你可以在项目根目录创建一个 `.env` 文件，一次性写死你的配置：

```ini
# .env 文件示例
BACKEND=cuda              # 强制使用显卡 (或 cpu)
COMPILE=1                 # 默认开启 10 倍速度优化
GRADIO_PORT=7860          # 更改 WebUI 的访问端口
API_PORT=8080             # 更改 API 服务的访问端口
GRADIO_SERVER_NAME=0.0.0.0 # 允许局域网其他设备访问
```

配置好 `.env` 文件后，直接运行 `docker compose --profile webui up` 即可自动读取。
