# 拆分指定页

```py
from pypdf import PdfReader, PdfWriter


def split_pdf_by_range(input_path, start_page, end_page, output_path):
    """
    拆分 PDF 的指定页码范围（页码从 1 开始）

    参数:
        input_path: 输入 PDF 路径
        start_page: 起始页码（包含）
        end_page: 结束页码（包含）
        output_path: 输出 PDF 路径
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # 注意：pypdf 中页码从 0 开始，需要减 1
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"已保存指定范围：{output_path}")


if __name__ == '__main__':
    # 拆分第 2-5 页
    split_pdf_by_range(
        "src.pdf",
        2, 5,
        "dst.pdf"
    )
```
