# 设置封面图

```py
from mutagen.id3 import ID3, APIC, error

mp3_path = "song.mp3"
cover_path = "cover.jpg"  # 也可以是 png

audio = ID3(mp3_path)

with open(cover_path, 'rb') as img:
    audio['APIC'] = APIC(
        encoding=3,         # UTF-8
        mime='image/jpeg',  # 或 'image/png'
        type=3,             # 3 = front cover
        desc='Cover',
        data=img.read()
    )

audio.save()
print("封面已写入")
```
