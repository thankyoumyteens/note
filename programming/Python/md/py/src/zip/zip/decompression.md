# 解压

```py
import zipfile
from pathlib import Path

def extract_zipfile(source_file_path, output_dir):
    with zipfile.ZipFile(source_file_path, "r") as zipf:
        zipf.extractall(output_dir)
```

## 指定压缩算法

```py
# 不压缩, 只打包
with zipfile.ZipFile(source_file_path, "r", compression=zipfile.ZIP_STORED) as zipf:
# zip
with zipfile.ZipFile(source_file_path, "r", compression=zipfile.ZIP_DEFLATED) as zipf:
# bzip2
with zipfile.ZipFile(source_file_path, "r", compression=zipfile.ZIP_BZIP2) as zipf:
# lzma
with zipfile.ZipFile(source_file_path, "r", compression=zipfile.ZIP_LZMA) as zipf:
```
