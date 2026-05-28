# 测试方式

### 启动 Java AI Gateway

正常路径：

```bash
mvn spring-boot:run
```

确认接口可用：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

预期：Java 接口正常返回 JSON。

---

### 安装 Python 依赖

```bash
cd python-tools
uv sync
```

预期：依赖安装成功。

---

### 运行 Python 调用脚本

```bash
uv run python scripts/call_chat.py
```

预期类似：

```json
{
  "answer": "RAG 是一种结合检索系统和大语言模型生成能力的技术。"
}
```

---

### 测试 Pydantic 校验

可以临时把 `ChatResponse` 改成错误字段名，例如：

```python
class ChatResponse(BaseModel):
    content: str
```

再运行：

```bash
uv run python scripts/call_chat.py
```

预期：Pydantic 报字段校验错误。

测试完恢复：

```python
class ChatResponse(BaseModel):
    answer: str = Field(min_length=1)
```

---

### 测试 base_url 配置

```bash
export AI_GATEWAY_BASE_URL="http://localhost:8080"
uv run python scripts/call_chat.py
```

预期：正常调用。

如果改成错误端口：

```bash
export AI_GATEWAY_BASE_URL="http://localhost:9999"
uv run python scripts/call_chat.py
```

预期：连接失败，证明配置生效。
