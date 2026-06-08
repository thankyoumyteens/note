# 新增 Tool Eval 数据集

评估 planner 是否选对工具、是否提取对参数。

第 7 课做过结构化输出 eval，第 13 课做过 RAG eval。

第 17 课开始做 tool eval：

```text
问题 -> plan -> requiredTool 是否正确
问题 -> plan -> arguments 是否正确
```

### 代码

文件：

```text
python-tools/tool_eval_cases.jsonl
```

```jsonl
{"id":"tool-001","title":"客户询问退款进度","description":"客户说订单 ORDER-1001 已经申请退款，但迟迟没有收到退款。","expectedTool":"checkOrder","expectedOrderId":"ORDER-1001"}
{"id":"tool-002","title":"订单退款风险确认","description":"请检查 ORDER-1001 是否存在重复退款风险。","expectedTool":"checkOrder","expectedOrderId":"ORDER-1001"}
```
