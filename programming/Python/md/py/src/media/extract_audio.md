# 从视频中提取音频

### 1. 安装

```sh
pip install moviepy
```

### 2. 运行

```py
from moviepy import AudioFileClip

clip = AudioFileClip('a.mp4')
clip.write_audiofile("output.mp3")
```
