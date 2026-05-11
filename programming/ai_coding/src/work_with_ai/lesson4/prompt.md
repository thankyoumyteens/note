# 推荐发给 Codex 的 Prompt

在项目根目录运行 Codex，然后发：

```text
目标：
新增文档保存功能，提供 POST /api/documents 接口保存文档标题和正文。

背景：
当前项目是 ai-doc-summary，已经完成最小 Spring Boot 项目、AGENTS.md、CLAUDE.md、.gitignore 和 Git baseline。
现在要进入第一个业务功能：文档保存。
本课目标是把模糊需求改写成清晰 AI 任务，并让 AI 先输出实现计划，不直接写代码。

输入：
请查看当前项目结构、README.md、pom.xml、AGENTS.md、CLAUDE.md、src/ 和 lessons/。

输出：
请先给出实现计划，不要直接修改代码。
输出内容包括：
1. 需求理解
2. 建议新增或修改的类
3. 接口请求 JSON 示例
4. 接口响应 JSON 示例
5. 内存存储设计
6. 参数校验策略
7. 测试计划
8. 风险点
9. 后续实现任务拆分

限制：
1. 暂时不要接入数据库，先用内存存储。
2. 不要接入 AI API。
3. 不要加入用户系统。
4. 不要加入 Spring Security。
5. 不要引入新依赖。
6. 不要实现文档查询接口。
7. 不要实现摘要生成接口。
8. 不要上传文件，只接收 JSON 请求体。
9. 不要修改任何项目文件，本课只输出计划。

验收标准：
1. 计划中明确 POST /api/documents 的请求 JSON 和响应 JSON。
2. 计划中明确标题和正文不能为空。
3. 计划中明确保存成功返回 documentId。
4. 计划中明确当前只使用内存存储。
5. 计划中明确不接数据库、不接 AI、不加用户系统。
6. 计划中包含测试覆盖：保存成功、标题为空、正文为空。
7. 计划中包含后续可执行的任务拆分。
8. 完成后请确认没有修改任何项目文件。
```

## 你应该期待 Codex 输出什么

理想输出不是代码，而是类似这样的计划。

```
1. 需求理解
新增业务能力：通过 POST /api/documents 接收 JSON 请求体，保存文档标题和正文，并返回新生成的 documentId。

当前阶段只做“保存”：

- 不接数据库，只用内存存储
- 不接 AI API
- 不加用户系统
- 不加 Spring Security
- 不实现文档查询接口
- 不实现摘要生成接口
- 不上传文件，只接收 JSON

标题和正文都不能为空；保存成功后返回 documentId。

2. 建议新增或修改的类
为了保持最小结构，但避免把业务继续堆到启动类里，建议新增少量类：

- DocumentController
    - 负责 POST /api/documents
    - 处理请求、调用内存存储、返回响应
- DocumentRequest
    - 请求 DTO：title、content
- DocumentResponse
    - 响应 DTO：documentId、title、content
- Document
    - 内存中的文档模型：id、title、content
- InMemoryDocumentStore
    - 使用内存 Map 保存文档
    - 使用 AtomicLong 或 UUID 生成 documentId

修改测试类或新增测试类：

- DocumentControllerTests
    - 覆盖保存成功、标题为空、正文为空

3. 接口请求 JSON 示例

{
"title": "Spring Boot 学习笔记",
"content": "这是一篇关于 Spring Boot 最小项目的文档正文。"
}

4. 接口响应 JSON 示例
建议成功返回 HTTP 201 Created：

{
"documentId": "1",
"title": "Spring Boot 学习笔记",
"content": "这是一篇关于 Spring Boot 最小项目的文档正文。"
}

参数错误建议返回 HTTP 400 Bad Request，响应可保持简单：

{
"error": "title must not be blank"
}

5. 内存存储设计
当前只使用进程内内存存储：

- ConcurrentHashMap<String, Document> 保存文档
- AtomicLong 递增生成 ID，例如 "1"、"2"、"3"
- 应用重启后数据丢失，这是当前阶段可接受的限制
- 暂不提供查询接口，所以存储只为后续课程扩展做准备

6. 参数校验策略
不引入新依赖。由于当前 pom.xml 没有 spring-boot-starter-validation，建议先手写校验：

- title == null || title.isBlank() 返回 400
- content == null || content.isBlank() 返回 400
- 可以在保存前 trim() 标题和正文，避免纯空格通过
- 暂不限制长度，后续需要时再补

7. 测试计划
使用现有 Spring Boot Test + MockMvc，不新增依赖。

测试覆盖：

- 保存成功
    - POST /api/documents
    - 请求包含非空 title 和 content
    - 期望 HTTP 201
    - 响应包含非空 documentId
    - 响应中的 title、content 与请求一致
- 标题为空
    - title 为 "" 或纯空格
    - 期望 HTTP 400
    - 响应包含错误信息
- 正文为空
    - content 为 "" 或纯空格
    - 期望 HTTP 400
    - 响应包含错误信息

同时保留已有健康检查测试，确保 GET /api/health 不受影响。

8. 风险点

- 内存存储不是持久化，应用重启后文档丢失。
- 多次测试可能共享 Spring 上下文中的内存数据，需要测试避免依赖固定 ID，或在测试中只断言 documentId 存在。
- 手写校验简单直接，但后续字段增多时可能需要引入 Bean Validation。
- 当前不实现查询接口，因此保存的数据暂时只能通过测试或后续功能验证。
- 如果把所有逻辑继续放在启动类里，会降低后续扩展性；建议从这个功能开始拆出最小 Controller 和 Store。

9. 后续实现任务拆分

1. 新增文档 DTO：DocumentRequest、DocumentResponse。
2. 新增领域模型：Document。
  3. 新增内存存储：InMemoryDocumentStore。
  4. 新增控制器：DocumentController，实现 POST /api/documents。
  5. 实现标题和正文非空校验，错误返回 400。
  6. 新增 MockMvc 测试：保存成功、标题为空、正文为空。
  7. 运行 mvn test。
  8. 手动启动 mvn spring-boot:run 后用 curl 验证接口。

  本次只输出计划，没有修改任何项目文件。
```

## 如果 Codex 直接改代码，如何纠正

发这个：

```text
本课是第 4 课：从模糊需求到清晰任务，只要求输出实现计划，不允许修改代码。

请回退本次对项目文件的修改，只保留文字计划。
然后重新输出：
1. 需求理解
2. 建议新增或修改的类
3. 请求 JSON
4. 响应 JSON
5. 内存存储设计
6. 参数校验策略
7. 测试计划
8. 风险点
9. 后续实现任务拆分
```

---

## 如果 Codex 的计划太复杂，如何纠正

比如它建议：

```text
JPA + H2 + Repository + Entity + Flyway
```

你就发：

```text
当前计划过度设计。第 4 课只需要文档保存功能的最小计划。

请重新规划，并遵守：
1. 不接数据库。
2. 不使用 JPA。
3. 不新增依赖。
4. 不实现查询接口。
5. 不实现摘要接口。
6. 只设计 POST /api/documents。
7. 存储方案使用内存 Map。
8. 输出计划，不修改代码。
```
