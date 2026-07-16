# 可靠的模型输出

这一阶段基于[最小 LLM 应用](../llm.md)已有的统一调用入口，把模型返回的自然语言转换为可以被程序解析、校验和处理的稳定输出。

本阶段不再重复 Provider 接入、超时、重试和降级，重点解决三个问题：

1. 使用 Prompt 明确任务、输入、约束和预期输出。
2. 使用结构化输出定义字段类型、枚举、必填项等输出契约。
3. 对模型结果执行解析、Schema 校验和业务校验，阻止非法结果进入后续业务调用。

先学习 [Prompt](./prompt/prompt.md)，理解角色设定、任务说明、变量、约束、Few-shot 示例和版本管理，再学习[结构化输出](./structure/structure.md)，理解 JSON Schema、原生结构化输出、结果校验和失败处理。

模型输出可能出现格式错误、字段缺失、Schema 不匹配和语义错误。应用需要区分这些失败类型，并根据场景选择拒绝结果、请求模型修复或有限次数重试，不能直接把模型返回值传给业务系统。

Prompt、Schema 或模型发生变化时，可以使用固定测试集比较结构化解析成功率、校验通过率、关键字段准确率和失败样本，判断变更是否提高了输出稳定性。

实现时沿用上一阶段选择的路线，在现有调用链上增加 Prompt 渲染、结构化输出约束和结果校验：

- [WebClient](../llm_api/spring_boot/spring_boot.md)：直接构造 Prompt 和 Provider 请求，并自行解析、校验返回结果。
- [Spring AI](../llm_api/spring_ai/spring_ai.md)：使用 PromptTemplate、结构化输出转换和模型抽象。
- [Python + uv](../llm_api/python/python.md)：使用 SDK 与数据校验模型，工程调用保持异步。
