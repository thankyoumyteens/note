# FaceFusion

1. 安装

```sh
brew install git
brew install miniconda
brew install ffmpeg

conda init --all
conda create --name facefusion python=3.10
conda activate facefusion
git clone https://github.com/facefusion/facefusion
cd facefusion
python install.py --onnxruntime default
conda deactivate
```

2. 运行

```sh
conda activate facefusion
python facefusion.py run
```
