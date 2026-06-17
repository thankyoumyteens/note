# 推荐事件协议

SSE 不要只返回裸文本，最好定义清楚事件类型。

推荐至少有：

- message：正常内容 chunk
- error：流式过程中发生错误
- done：正常结束
- heartbeat：心跳

前端逻辑应该是：

```text
收到 message → 追加内容
收到 heartbeat → 不展示
收到 error → 展示错误并关闭连接
收到 done → 正常结束
连接异常关闭但没收到 done → 视为异常断流
```
