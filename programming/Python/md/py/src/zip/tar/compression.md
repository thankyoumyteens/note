# 压缩

目录结构:

```
demo_dir
├── 1.txt
└── 2
    └── 3.txt
```

## 压缩指定目录下所有文件和文件夹(不包含文件夹)

```py
import tarfile
from pathlib import Path

def make_tarfile(source_dir, output_file_path):
    with tarfile.open(output_file_path, "w") as tar:
        for path in source_dir.glob("**/*"):
            relative_path = path.relative_to(source_dir)
            if path.is_file():
                tar.add(str(path), arcname=str(relative_path))
```

tar 包中的结构:

```
1.txt
2/3.txt
```

## 压缩指定目录下所有文件和文件夹(包含文件夹)

```py
import tarfile
from pathlib import Path

def make_tarfile(source_dir, output_file_path):
    with tarfile.open(output_file_path, "w") as tar:
        for path in source_dir.glob("**/*"):
            relative_path = path.relative_to(source_dir)
            if path.is_file():
                # 手动把外层文件夹拼上
                tar.add(str(path), arcname=f"{str(source_dir.name)}/{str(relative_path)}")
```

```
demo_dir/1.txt
demo_dir/2/3.txt
```

## 指定压缩算法

```py
# 不压缩, 只打包
with tarfile.open(output_file_path, "w") as tar:
# gzip
with tarfile.open(output_file_path, "w:gz") as tar:
# bzip2
with tarfile.open(output_file_path, "w:bz2") as tar:
# lzma
with tarfile.open(output_file_path, "w:xz") as tar:
```
