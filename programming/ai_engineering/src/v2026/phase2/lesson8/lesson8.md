# 第 8 课：AI Gateway 生产化

前面你已经完成：

```text
/api/ai/chat
/api/ai/chat/stream
/api/ai/extract-task
/api/ai/order-assistant
evals/
```

现在的问题是：系统虽然能跑，但还不够“生产化”。

生产化不是“接口能跑通”。

生产化意味着你能回答这些问题：

```text
这次模型调用用了哪个模型？
耗时多少？
成功还是失败？
失败原因是什么？
用了多少 token？
是哪类调用？
是否触发了工具？
调用了哪个工具？
工具参数是什么？
工具执行成功了吗？
```

没有这些信息，后续排查会很困难。
