# 搭建ChatTTS环境

### 一、 基础环境与依赖准备

ChatTTS 基于 PyTorch 构建，强烈依赖显卡算力来保证生成速度。

**1. 克隆项目与配置虚拟环境**
推荐使用 Conda 隔离环境，保持系统纯净：

```bash
git clone https://github.com/2noise/ChatTTS.git
cd ChatTTS
conda create -n chattts python=3.10
conda activate chattts
```

**2. 安装核心依赖**
必须安装支持 CUDA 的 PyTorch 版本，以充分调用 GPU：

```bash
# 安装 PyTorch (根据你的 CUDA 版本调整)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130

# 安装 ChatTTS 依赖
pip install -r requirements.txt
# 在 Windows 环境下，最新版 torchaudio 的默认保存后端有时会引发依赖缺失问题。
# 相比去折腾复杂的 Windows 音频编码库编译，最简单且业界最通用的做法是换用 soundfile 库来保存 WAV 文件。
pip install soundfile
```

---

### 二、 模型的下载与基础使用

ChatTTS 支持从 HuggingFace 或 ModelScope 自动拉取模型。初次运行时，代码会自动下载模型权重。

**最小化 Python 调用示例：**
创建一个 `test_tts.py` 文件，这是最基础的本地生成链路。

```python
import ChatTTS
import soundfile as sf

# 1. 初始化 ChatTTS 实例
chat = ChatTTS.Chat()
# 强制使用 GPU，并加载模型
chat.load(compile=False)

# 2. 准备文本
texts = [
    "你好啊! [laugh] 很高兴今天能和你聊天。",
    "不过... [uv_break] 我们得先处理一下后端的逻辑。"
]

# 3. 推理生成音频
print("正在生成音频，请稍候...")
wavs = chat.infer(texts, use_decoder=True)

# 4. 保存为 WAV 文件 (使用 soundfile)
for i, wav in enumerate(wavs):
    # ChatTTS 返回的 wav 通常是 numpy 数组
    # 使用 .squeeze() 去除多余的维度，使其变成一维数组，方便 soundfile 写入
    audio_data = wav.squeeze()

    # sf.write 参数：文件名, 音频数据, 采样率(24000)
    sf.write(f"output_{i}.wav", audio_data, 24000)
    print(f"✅ 已成功保存 output_{i}.wav")
```
