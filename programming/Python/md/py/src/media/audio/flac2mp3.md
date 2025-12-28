# flac 转 mp3

```py
from pydub import AudioSegment

# 输入输出路径
flac_path = "input.flac"
mp3_path = "output.mp3"

# 读取 flac
audio = AudioSegment.from_file(flac_path, format="flac")

# 导出为 mp3，设置比特率
audio.export(mp3_path, format="mp3", bitrate="320k")
print("转换完成：", mp3_path)
```
