# 提取封面图

```py
from mutagen.id3 import ID3
import os

def extract_cover(mp3_path, out_path=None):
    audio = ID3(mp3_path)

    # 找到第一个 APIC(封面)帧
    apic_list = [f for f in audio.values() if f.FrameID == "APIC"]
    if not apic_list:
        print("没有找到封面图标签(APIC)。")
        return

    apic = apic_list[0]
    mime = apic.mime  # 例如 'image/jpeg' 或 'image/png'
    data = apic.data  # 图片二进制数据

    # 自动推断扩展名
    if out_path is None:
        ext = ".jpg"
        if mime == "image/png":
            ext = ".png"
        elif mime == "image/jpeg":
            ext = ".jpg"
        elif mime == "image/webp":
            ext = ".webp"

        base = os.path.splitext(os.path.basename(mp3_path))[0]
        out_path = base + "_cover" + ext

    with open(out_path, "wb") as f:
        f.write(data)

    print(f"封面已保存为: {out_path}")

# 使用示例
extract_cover("song.mp3")
```
