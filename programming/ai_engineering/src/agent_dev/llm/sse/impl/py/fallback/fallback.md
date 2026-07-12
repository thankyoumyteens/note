# 重试和降级

核心差异：

- 普通 API：失败后可以整体 retry / fallback
- SSE：只有还没输出任何 message chunk 前，才可以 retry / fallback
