# 本课推荐 Prompt

在项目根目录打开 Codex，发送下面这段：

```text
目标：
围绕文档保存功能，练习 AI 输出格式控制。

背景：
当前项目是 ai-doc-summary，已经完成最小 Spring Boot 项目、AGENTS.md、CLAUDE.md、Git baseline，并完成了第 4 课的文档保存功能计划。
第 4 课明确：后续要实现 POST /api/documents，接收 title 和 content，成功后返回 documentId；当前阶段只使用内存存储，不接数据库、不接 AI API、不加用户系统、不加 Spring Security、不新增依赖。

输入：
请参考当前项目代码、AGENTS.md、CLAUDE.md、README.md，以及第 4 课的文档保存计划。

输出：
请不要修改任何项目文件。
请只输出以下 5 个部分，并使用 Markdown 标题分区：

## 1. 产品解释
用非技术语言解释文档保存功能，面向产品经理或业务方。

## 2. 开发计划
用开发者视角输出实现计划，包括建议新增类、主要方法、接口路径、状态码和实现步骤。

## 3. 接口 JSON 示例
输出请求 JSON、成功响应 JSON、参数错误响应 JSON。
JSON 必须放在代码块中。
成功响应第一版只返回 documentId，不返回完整 content。

## 4. 测试用例清单
使用 Markdown checkbox 格式。
至少包含：
- 保存成功
- title 为空
- title 为空格
- content 为空
- content 为空格
- 健康检查接口不受影响

## 5. 代码审查 Checklist
使用 Markdown checkbox 格式。
重点检查：
- 是否未引入数据库
- 是否未引入 AI API
- 是否未引入 Spring Security
- 是否未新增依赖
- 是否没有修改无关文件
- 是否有测试覆盖
- 是否响应格式符合约定

限制：
1. 不要修改任何项目文件。
2. 不要输出 Java 代码实现。
3. 不要创建新文件。
4. 不要运行命令。
5. 不要接入数据库、AI API、用户系统、Spring Security 或新依赖。
6. 不要把响应设计扩展得过复杂。
7. 成功响应只返回 documentId。

验收标准：
1. 输出严格分为 5 个 Markdown 章节。
2. JSON 示例放在代码块中。
3. 测试用例清单使用 checkbox。
4. Review checklist 使用 checkbox。
5. 成功响应只包含 documentId。
6. 没有修改任何项目文件。
```

## 你要检查 AI 输出的重点

检查这 7 点：

```text
1. 是否严格分成 5 个章节
2. 产品解释是否适合非技术人员
3. 开发计划是否可执行
4. JSON 是否放在代码块中
5. 成功响应是否只返回 documentId
6. 测试清单是否用 checkbox
7. Review checklist 是否用 checkbox
```

如果 Codex 输出了 Java 实现代码，说明它越界了。

如果 Codex 创建或修改了文件，也说明它越界了。

## 如果 Codex 输出太散，怎么纠正

发这个：

```text
输出格式不符合第 5 课要求。请重新输出。

要求：
1. 严格使用 5 个 Markdown 二级标题：
   ## 1. 产品解释
   ## 2. 开发计划
   ## 3. 接口 JSON 示例
   ## 4. 测试用例清单
   ## 5. 代码审查 Checklist
2. JSON 必须放在代码块中。
3. 测试用例清单必须使用 - [ ] checkbox。
4. 代码审查 Checklist 必须使用 - [ ] checkbox。
5. 不要输出 Java 实现代码。
6. 不要修改任何项目文件。
```

## 如果 Codex 又想修改代码，怎么纠正

发这个：

```text
本课是第 5 课：输出格式控制，只练习输出结构，不允许修改代码。

请停止修改文件。
请不要创建新文件。
请只在对话中输出 5 个 Markdown 章节：
1. 产品解释
2. 开发计划
3. 接口 JSON 示例
4. 测试用例清单
5. 代码审查 Checklist
```
