# 给 Python 客户端加上探针

在你的 Python 项目根目录下，修改或创建 `.env` 文件（这是绝对核心的一步）：

```conf
# 填入你刚才在本地 3000 端口生成的 Key
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
# 把探头数据打到本地容器！
LANGFUSE_HOST=http://localhost:3000
```
