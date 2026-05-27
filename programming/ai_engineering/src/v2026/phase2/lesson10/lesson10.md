# 第 10 课：Python AI 工具补齐

前面 Java 主线已经完成 AI Gateway、结构化输出、Tool Calling、Evals、生产化、Spring AI 适配。现在需要补齐 Python 辅助工具能力。

一句话概括：

> 本课建立 `python-tools/`，用 uv、httpx、Pydantic 做一个最小 Python 工具包，用来调用 Java AI Gateway、校验响应结构、批量处理数据，为后续 RAG 和 eval 做准备。

## 技术选择

```text
uv        Python 项目和依赖管理
httpx     HTTP Client
Pydantic  请求 / 响应 DTO 校验
```

uv 是 Astral 官方维护的 Python package/project manager；HTTPX 官方文档说明它提供同步 API，也支持 async client，且默认带 timeout；Pydantic 的 `BaseModel` 用于定义字段模型，`model_validate` / `model_validate_json` 可用于校验对象或 JSON 数据。
