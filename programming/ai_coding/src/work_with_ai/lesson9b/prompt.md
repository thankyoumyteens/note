# 本课推荐 Prompt

````text
目标：
使用 spec-workflow-mcp 管理并实现一个功能：

`GET /api/documents/{id}/metadata`

任务目标：
使用 spec-workflow-mcp 创建并推进 feature spec。
请不要手写普通 `specs/` 目录。
请优先使用 spec-workflow-mcp 提供的工具创建和推进 feature。

背景：
当前项目是 `ai-doc-summary`，已经完成：

1. `POST /api/documents` 文档保存功能。
2. `GET /api/documents/{id}` 文档查询功能。
3. 当前项目已经具备手写轻量 spec 的经验。
4. 当前项目已经安装或配置过 `spec-workflow-mcp`。

功能说明：
新增接口：

`GET /api/documents/{id}/metadata`

成功时返回文档元信息，不返回 `content`：

```json
{
  "documentId": "1",
  "title": "Spring Boot 学习笔记",
  "contentLength": 28
}
```

`documentId` 不存在时返回 `404 Not Found`。

功能约束：

1. 只实现 `GET /api/documents/{id}/metadata`。
2. 成功响应不返回 `content`。
3. 成功响应包含 `documentId`、`title`、`contentLength`。
4. `contentLength` 使用 `content` 的字符长度。
5. `documentId` 不存在时返回 `404 Not Found`。
6. 继续只使用内存存储。
7. 不接数据库。
8. 不使用 JPA。
9. 不新增 Java 依赖。
10. 不接真实 AI API。
11. 不加入 Spring AI。
12. 不加入 Spring Security。
13. 不加入用户系统。
14. 不实现搜索。
15. 不实现分页。
16. 不实现文件上传。
17. 不实现摘要生成。

执行流程：

1. 先检查 spec-workflow-mcp 是否可用。
2. 使用 spec-workflow-mcp 创建 feature spec，建议 feature 名称为 `document-metadata`。
3. 生成或完善 requirements。
4. 生成或完善 design。
5. 生成或完善 tasks。
6. 如果工具有 approval 流程，请按工具要求完成审批，或说明需要人工确认。
7. 按 tasks 逐项实现。
8. 每完成一个 task，使用 MCP 工具更新 task 状态，不要最后统一更新。

执行节奏：
每次只执行当前第一个未完成 task。
完成当前 task 后必须停止，输出状态，等待我确认。
我没有明确说“继续”之前，不允许执行下一个 task。

实现要求：

1. 复用已有 document 存储能力。
2. 如需给 `InMemoryDocumentStore` 增加查询或 metadata 支持，保持最小修改。
3. 如需新增响应 DTO，可以新增 `DocumentMetadataResponse` 或等价命名。
4. 如需修改 Controller，保持接口最小。
5. 不要引入 Service 层，除非已有代码结构已经需要。
6. 不要改 `pom.xml`。
7. 不要新增依赖。

测试要求：
至少覆盖：

1. 查询已存在文档 metadata 成功。
2. 成功响应包含 `documentId`、`title`、`contentLength`。
3. 成功响应不包含 `content`。
4. 查询不存在 `documentId` 返回 `404`。
5. 已有 `POST /api/documents` 测试不受影响。
6. 已有 `GET /api/documents/{id}` 测试不受影响。
7. 健康检查接口 `GET /api/health` 不受影响。

最终验收：

1. `GET /api/documents/{id}/metadata` 可用。
2. 成功响应不返回 `content`。
3. `contentLength` 正确。
4. 不存在返回 `404`。
5. `mvn test` 通过。
6. MCP 中的 feature tasks 状态与实际代码进度一致。
7. 没有修改 `pom.xml`。
8. 没有新增 Java 依赖。
9. 没有引入数据库 / JPA / Spring AI / 真实 AI API / Security / 用户系统。
10. 不执行 `git add`。
11. 不执行 `git commit`。
````
