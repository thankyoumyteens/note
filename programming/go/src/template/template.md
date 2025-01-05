# 模版渲染

Go 语言提供了两个包进行模板渲染

- `html/template` 针对的是需要返回 HTML 内容的场景, 在模板渲染过程中会对一些有风险的内容进行转义
- `text/template` 将内容都按 text 文本格式返回
