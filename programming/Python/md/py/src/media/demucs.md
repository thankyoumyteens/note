# 人声和伴奏分离

python 版本: python 3.12。

### 1. 安装

```sh
pip install --user -U demucs
```

### 2. 运行

```py
from demucs.separate import main as demucs_separate

# 构造参数
args = [
    './a.mp3',  # 输入音频路径（必须是第一个参数）
    "--out", "~/Downloads",  # 输出目录
    "--two-stems", "vocals",  # 只分人声和伴奏
    "--device", "cpu",  # 运行设备
    "--mp3",  # 输出为 MP3 格式
    "--mp3-bitrate", "320"  # MP3 比特率（可选）
]

# 模拟命令行参数传入
sys.argv = ["demucs"] + args
# 执行
demucs_separate()

print('分离完成')
```
