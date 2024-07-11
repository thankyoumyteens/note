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
import zipfile
from pathlib import Path

def make_zipfile(source_dir, output_file_path):
    with zipfile.ZipFile(output_file_path, "w") as zipf:
        for path in source_dir.glob("**/*"):
            relative_path = path.relative_to(source_dir)
            if path.is_file():
                zipf.write(str(path), arcname=f"{str(relative_path)}")
```

zip 包中的结构:

```
1.txt
2/3.txt
```

## 压缩指定目录下所有文件和文件夹(包含文件夹)

```py
import zipfile
from pathlib import Path

def make_zipfile(source_dir, output_file_path):
    with zipfile.ZipFile(output_file_path, "w") as zipf:
        for path in source_dir.glob("**/*"):
            relative_path = path.relative_to(source_dir)
            if path.is_file():
                # 手动把外层文件夹拼上
                zipf.write(str(path), arcname=f"{str(source_dir.name)}/{str(relative_path)}")
```

```
demo_dir/1.txt
demo_dir/2/3.txt
```

## 指定压缩算法

```py
# 不压缩, 只打包
with zipfile.ZipFile(output_file_path, "w", compression=zipfile.ZIP_STORED) as zipf:
# zip
with zipfile.ZipFile(output_file_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
# bzip2
with zipfile.ZipFile(output_file_path, "w", compression=zipfile.ZIP_BZIP2) as zipf:
# lzma
with zipfile.ZipFile(output_file_path, "w", compression=zipfile.ZIP_LZMA) as zipf:
```
