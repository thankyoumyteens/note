# 第五步：最终 diff 审查

最后让 Codex 审查当前 diff：

```text
目标：
第 9 课最终检查。请审查当前 git diff，不要修改任何文件。

请检查：
1. 是否实现了 GET /api/documents/{id}
2. 查询成功是否返回 200 OK
3. 成功响应是否包含 documentId、title、content
4. 查询不存在是否返回 404 Not Found
5. 是否没有改变 POST /api/documents 成功响应格式
6. 是否没有修改 pom.xml
7. 是否没有新增依赖
8. 是否没有接入数据库
9. 是否没有接入 AI API
10. 是否没有加入用户系统或 Spring Security
11. 是否没有实现列表查询或摘要功能
12. 是否更新了 specs/document-query/tasks.md
13. 是否有测试覆盖成功查询和不存在查询
14. mvn test 是否通过
15. 是否有无关文件修改或过度设计

请按以下格式输出：
## 符合要求
## 需要修正
## 风险提示
## 建议提交信息

限制：
不要修改文件。
```
