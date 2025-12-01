# 设置 ID3 标签

ID3 标签是一种为音频文件（主要是 MP3）嵌入和存储元数据（metadata）的格式。它允许将曲目名称、艺术家、专辑、年份和流派等信息直接保存在音频文件内，方便管理和识别。

```py
from mutagen.easyid3 import EasyID3

file = "song.mp3"

try:
    # 获取文件的 ID3 标签
    audio = EasyID3(file)
except Exception:
    # 文件还没有 ID3 标签，需要先创建
    from mutagen.id3 import ID3
    # 新建一个空 ID3 标签
    audio = EasyID3()
    audio.save(file)
    # 重新获取 ID3 标签
    audio = EasyID3(file)

# 设置曲目名称、艺术家、专辑、年份和流派
audio['title'] = "新标题"
audio['artist'] = "演唱者名字"
audio['album'] = "专辑名"
audio['date'] = "2024"
audio['genre'] = "Rock"

audio.save()
print("修改完成")
```
