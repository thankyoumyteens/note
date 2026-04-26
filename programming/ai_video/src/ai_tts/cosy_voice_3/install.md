# 搭建 CosyVoice 3.0 环境

搭建 CosyVoice 环境的最佳实践是优先使用 Docker 容器化部署以避免复杂的 C++ 音频底层依赖库冲突。

请注意：**运行 AI 模型需要显卡加速 (GPU)**，在 Docker 中使用 GPU 必须通过 **WSL2** (Windows Subsystem for Linux)。

以下是使用 Docker 部署 `CosyVoice` 的最简方案：

### 第一步：检查基础环境（非常重要）

在开始之前，确保你的电脑满足以下条件：

1.  **安装 Docker Desktop**：如果还没安装，请去 [Docker 官网](https://www.docker.com/products/docker-desktop/) 下载并安装。
2.  **WSL2 后端**：确保 Docker Desktop 设置中开启了 WSL2 支持。
3.  **NVIDIA Container Toolkit**：这是在 Docker 中调用 GPU 的关键。
    - 在 Windows 上，只要你的 NVIDIA 驱动已更新且 Docker Desktop 配置正确，通常会自动支持。
    - **验证方法**：在 Windows 命令行（PowerShell）中输入 `docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi`。如果能看到显卡信息，说明 GPU 在 Docker 中已打通。

---

### 第二步：一键运行 (使用第三方封装的镜像)

社区已经有封装好的镜像（包含 WebUI 和 API），比自己从零构建要简单得多。我们将使用 `neosun100/cosyvoice` 这个版本，它是目前部署最方便的方案：

在 PowerShell 中运行以下命令：

```sh
# 1. 创建存放语音数据的文件夹 (为了持久化保存你的克隆音色)
mkdir cosyvoice-data

# 2. 启动容器 (包含 GPU 支持)
docker run -d `
  --name cosyvoice `
  --gpus all `
  -p 8188:8188 `
  -v ./cosyvoice-data:/data/voices `
  --restart unless-stopped `
  neosun/cosyvoice:v3.4.0
```

- **参数解释**：
  - `--gpus all`: 强制使用你的 NVIDIA 显卡。
  - `-p 8188:8188`: 将容器的 8188 端口映射到电脑的 8188。
  - `-v ./cosyvoice-data:/data/voices`: 将你的文件夹映射进容器，这样数据不会因为重启而丢失。

---

### 第三步：开始使用

等待几分钟（Docker 会自动下载几 GB 的镜像），一旦下载完成，你的 CosyVoice 服务就运行起来了。

1.  **打开浏览器**：访问 `http://localhost:8188`。
2.  **如果无法访问**：请检查 Docker Desktop 的容器日志（在 Docker Dashboard 中点击该容器查看 Logs），确保没有报错。
