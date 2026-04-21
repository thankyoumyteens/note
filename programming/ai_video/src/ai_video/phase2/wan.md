# Wan 2.2 14B

### 一、 创建 DiT 视频专属 Conda 环境

为了防止百亿参数视频大模型的底层依赖（尤其是特定版本的 `diffusers` 和 `transformers`）与你现有的 ComfyUI 环境发生冲突，我们必须像你之前做的那样，进行物理隔离。

```bash
conda create -n wan_video python=3.11
conda activate wan_video
```

_(激活后，命令行提示符前会出现 `(wan_video)` 标志)_

### 二、 部署支持 RTX 5090 的满血 PyTorch

我们直接打入支持最新架构的 CUDA 13.0 组合，彻底释放 5090 的算力：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

### 三、 安装原生视频大模型依赖

不同于 ComfyUI 满屏的节点，调用原生 DiT 模型只需要这几个业界标准的 Python 核心库：

```bash
pip install diffusers transformers accelerate huggingface_hub peft imageio[ffmpeg] xformers ftfy
```

### 四、 开启国内镜像并拉取 14B 巨兽模型

Wan 2.2 14B 的完整权重非常大。我们通过设置环境变量启用镜像加速，并开启断点续传。

_(注意：以下环境变量的写法适用于 Anaconda Prompt / CMD。请确保 `D:\Models` 目录有至少 50GB 空间，你也可以自行修改路径)_

```cmd
# 临时取消代理
set http_proxy=
set https_proxy=
set all_proxy=

# 1. 设置系统环境变量，指向国内的高速镜像节点
set HF_ENDPOINT=https://hf-mirror.com

# 2. 使用 CLI 工具全速拉取模型 (支持断点续传)
hf download Wan-AI/Wan2.1-I2V-14B-720P-Diffusers --local-dir C:\Users\ILove\software\ai_video\Wan\Wan-14B-I2V-720P --max-workers 16
```

直接敲回车跑起来，即使中途不小心关掉了终端或者断网，再次输入这行相同的命令，它就会自动从断点继续全速下载！

等控制台的进度条跑完，提示 `Download completed`。

### 五、 设置虚拟内存

1. 按下 `Win` 键，搜索并打开 **查看高级系统设置**。
2. 点击 **性能** -> **设置** -> **高级** -> **虚拟内存 (更改)**。
3. 选中你的 **C 盘**。
4. 选择 **自定义大小**，填入以下极其精确的数字（128GB 换算成 MB）：
   - **初始大小 (MB)**：`131072`
   - **最大值 (MB)**：`131072`
     _(注意：务必让初始大小和最大值保持完全一致，这样 Windows 在开机时就会直接锁死这块物理扇区，绝不会产生拖慢速度的磁盘碎片。)_
5. **极其关键**：点击右侧的 **[设置(S)]** 按钮。
6. 点击 **确定**。

**最后一步，也是最重要的一步：立刻重启电脑！**
