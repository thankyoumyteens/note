# 基本使用

```py
import markdown


def markdown_to_html(markdown_text):
    # 将 Markdown 文本转换为 HTML
    html = markdown.markdown(markdown_text)
    return html


# 使用示例
if __name__ == "__main__":
    markdown_content = r"""
# 标题一

这是一个**粗体文本**和*斜体文本*。

- 列表项1
- 列表项2

[链接](https://example.com)
"""
    html_output = markdown_to_html(markdown_content)
    print(html_output)
```
