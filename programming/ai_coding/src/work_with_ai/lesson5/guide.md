# 不符合预期怎么纠正

## 如果 Claude Code 输出太散，怎么纠正

如果它没有严格分 5 个章节，发这个：

```text
输出格式不符合第 5 课要求。请重新输出。

要求：
1. 严格使用以下 5 个 Markdown 二级标题：
   ## 1. 产品解释
   ## 2. 开发计划
   ## 3. 接口 JSON 示例
   ## 4. 测试用例清单
   ## 5. Code Review Checklist
2. JSON 必须放在代码块中。
3. 测试用例清单必须使用 - [ ] checkbox。
4. Code Review Checklist 必须使用 - [ ] checkbox。
5. 成功响应只返回 documentId。
6. 不要输出 Java 实现代码。
7. 不要修改任何项目文件。
```

---

## 如果 Claude Code 想改代码，怎么纠正

发这个：

```text
本课是第 5 课：输出格式控制，只练习输出结构，不允许修改代码。

请停止修改文件。
请不要创建新文件。
请不要运行命令。
请只在对话中输出 5 个 Markdown 章节：
1. 产品解释
2. 开发计划
3. 接口 JSON 示例
4. 测试用例清单
5. Code Review Checklist
```
