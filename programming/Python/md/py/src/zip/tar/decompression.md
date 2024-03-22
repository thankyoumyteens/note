# 解压

```py
import tarfile
from pathlib import Path

def extract_tarfile(source_file_path, output_dir):
    with tarfile.open(source_file_path, "r") as tar:
        tar.extractall(output_dir)
```

## 指定压缩算法

```py
# 不压缩, 只打包
with tarfile.open(output_file_path, "r") as tar:
# gzip
with tarfile.open(source_file_path, "r:gz") as tar:
# bzip2
with tarfile.open(source_file_path, "r:bz2") as tar:
# lzma
with tarfile.open(source_file_path, "r:xz") as tar:
```
