# LivePortrait

1. 环境搭建

```sh
git clone https://github.com/KwaiVGI/LivePortrait
cd LivePortrait

# 使用conda创建环境
conda create -n LivePortrait python=3.9
conda activate LivePortrait

# 对于搭载Apple Silicon的macOS用户
pip install -r requirements_macOS.txt
```

2. 下载预训练权重

```sh
# 从HuggingFace下载
# !pip install -U "huggingface_hub[cli]"
huggingface-cli download KwaiVGI/LivePortrait --local-dir pretrained_weights --exclude "*.git*" "README.md" "docs"

# 从镜像网站下载
# !pip install -U "huggingface_hub[cli]"
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download KwaiVGI/LivePortrait --local-dir pretrained_weights --exclude "*.git*" "README.md" "docs"
```

3. 测试

```sh
# 对于搭载Apple Silicon的macOS用户（Intel未测试）。注意：这可能比RTX 4090慢20倍
PYTORCH_ENABLE_MPS_FALLBACK=1 python inference.py
```

## Gradio 界面

```sh
pip install https://gradio-pypi-previews.s3.amazonaws.com/c5d763c3305fc143ace9ca6f8bdc32f12cef74d1/gradio-4.42.0-py3-none-any.whl
pip install "gradio-client @ git+https://github.com/gradio-app/gradio@c5d763c3305fc143ace9ca6f8bdc32f12cef74d1#subdirectory=client/python"
npm install https://gradio-npm-previews.s3.amazonaws.com/c5d763c3305fc143ace9ca6f8bdc32f12cef74d1/gradio-client-1.5.1.tgz

# 对于搭载Apple Silicon的macOS用户，不支持Intel，这可能比RTX 4090慢20倍
PYTORCH_ENABLE_MPS_FALLBACK=1 python app.py # 人类模型模式
```
