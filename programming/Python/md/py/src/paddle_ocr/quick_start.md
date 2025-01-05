# 基本使用

### 1.安装

```sh
pip install setuptools
pip install paddlepaddle==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
pip install paddleocr
```

### 2. 使用

```py
from paddleocr import PaddleOCR

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# whl包会自动下载ppocr轻量级模型作为默认模型
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
img_path = './demo.png'
# 结果是一个list, 每个item包含了文本框, 文字和识别置信度
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)
```
