# 旋转页面

```py
from pypdf import PdfReader, PdfWriter


def rotate_pdf_pages(input_path, output_path, page_numbers, rotation_angle):
    """
    旋转 PDF 中指定的页面

    参数:
        input_path: 输入 PDF 路径
        output_path: 输出 PDF 路径
        page_numbers: 要旋转的页码列表（页码从 1 开始，如 [1, 3] 表示第1、3页）
        rotation_angle: 旋转角度（90 的倍数，正数顺时针，负数逆时针）
    """
    # 读取原始 PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # 遍历所有页面
    for page_idx in range(len(reader.pages)):
        page = reader.pages[page_idx]
        # 检查当前页是否在需旋转的列表中（注意：代码中页码从 0 开始，需+1转换）
        if (page_idx + 1) in page_numbers:
            # 旋转页面
            page.rotate(rotation_angle)
        # 添加到新 PDF 中
        writer.add_page(page)

    # 保存结果
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"已保存旋转后的 PDF：{output_path}")


if __name__ == '__main__':
    rotate_pdf_pages(
        "src.pdf",
        "dst.pdf",
        page_numbers=[2, 4],  # 旋转第 2 页和第 4 页
        rotation_angle=180  # 顺时针旋转 180°
    )
```

注意: 旋转角度必须是 90 的倍数（如 90、180、270、-90 等），否则可能导致异常。
