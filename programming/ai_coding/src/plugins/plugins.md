# MCP

MCP（Model Context Protocol，模型上下文协议）是一套连接 AI 应用与外部系统的开放协议。

可以把 MCP 理解成 AI 工具生态中的“通用接口”：AI Client 不需要为每个数据库、代码仓库或业务系统分别设计一套接入方式，只要双方都支持 MCP，就可以通过统一协议交换上下文、调用工具和使用 Prompt 模板。

常见的 MCP Client 包括 Codex CLI、Claude Code、Gemini CLI、OpenCode 等。MCP Server 则负责对外提供具体能力，例如读取项目资料、查询数据库、操作 GitHub 或管理 Spec Workflow。

## MCP 的基本结构

一次 MCP 交互通常包含三个角色：

1. **Host**：承载 AI 对话和 Agent 的应用，例如 AI Coding 工具或 IDE。
2. **Client**：由 Host 创建，负责与某个 MCP Server 建立连接并交换协议消息。
3. **Server**：提供 Tools、Resources、Prompts 等能力的独立程序或远程服务。

可以简单理解为：

```text
用户
  ↓
AI Coding 工具（Host）
  ↓
MCP Client
  ↓ MCP 协议
MCP Server
  ↓
数据库、文件、GitHub、业务 API 等外部系统
```

MCP 只规定通信方式和能力描述方式，并不规定 Server 必须使用哪种编程语言，也不代表模型可以绕过客户端权限直接操作外部系统。

## MCP Server 可以提供什么

MCP Server 主要可以提供三类能力：

| 能力      | 作用                     | 常见示例                                | 主要控制方 |
| --------- | ------------------------ | --------------------------------------- | ---------- |
| Tools     | 让模型执行函数           | 查询数据库、写文件、调用 API、审批 Spec | 模型       |
| Resources | 向模型提供上下文数据     | 文件内容、数据库结构、API 文档、知识库  | 客户端应用 |
| Prompts   | 提供预定义的 Prompt 模板 | 代码评审、需求分析、生成设计文档        | 用户       |

实际使用中，Tools 最常见，Resources 和 Prompts 是否容易使用，还取决于 MCP Client 的支持情况和交互设计。

## Tools 是什么

Tool 是 MCP Server 暴露给模型调用的函数。每个 Tool 通常包含：

- 名称，例如 `search_documents`。
- 功能描述，帮助模型判断什么时候调用。
- 输入参数，通常使用 JSON Schema 描述。
- 执行结果，可以是文本、结构化数据、图片或 Resource 链接。

例如，一个数据库 MCP Server 可以提供：

```js
read_text_from_db(topic: string)
save_text_to_db(topic: string, content: string)
```

当用户说“查询之前保存的后端规范”时，模型可以决定调用：

```js
read_text_from_db((topic = "backend-specs"));
```

Tool 不一定会修改外部系统。只读的搜索和查询也可以设计成 Tool。判断重点不是“读还是写”，而是模型是否需要主动选择操作并生成调用参数。

## Resources 是什么

Resource 是 MCP Server 提供的、可以通过 URI 定位的上下文数据，例如：

```text
file:///project/AGENTS.md
docs://api/authentication
schema://database/users
memory://backend-specs
```

客户端通常通过下面的协议操作发现和读取 Resource：

```text
resources/list
resources/templates/list
resources/read
```

Resource 可以是固定 URI，也可以使用 URI Template 表达动态资源：

```text
docs://modules/{module}
memory://topics/{topic}
```

Resources 更适合表达“可发现、可选择、可重复读取的资料”。MCP Client 可以让用户选择资源，也可以根据当前任务自动选择并加载相关内容。

## Resources 和 Tools 的区别

可以用一句话区分：

> 如果希望 AI 做一件事，优先考虑 Tool；如果希望客户端给 AI 一份资料，优先考虑 Resource。

| 对比项   | Resources                          | Tools                        |
| -------- | ---------------------------------- | ---------------------------- |
| 核心作用 | 提供上下文和资料                   | 执行操作或查询               |
| 标识方式 | URI                                | Tool 名称                    |
| 参数形式 | 固定 URI 或 URI Template           | JSON Schema 参数             |
| 常用操作 | `resources/list`、`resources/read` | `tools/list`、`tools/call`   |
| 使用方式 | 主要由客户端发现、选择和加载       | 主要由模型判断并调用         |
| 副作用   | 通常用于只读访问                   | 可能读取，也可能修改外部系统 |

“读取数据”不一定要设计成 Resource。例如：

```js
search_database((keyword = "MCP"), (limit = 10));
```

这是一次由模型发起、带有查询参数的主动操作，因此适合设计成 Tool。

下面这种稳定、可寻址的资料更适合设计成 Resource：

```text
docs://mcp/introduction
```

两者也可以组合使用。例如模型先调用 `search_documents` Tool，Tool 返回匹配文档的 Resource URI，客户端再按需读取完整内容。

## 为什么很多 MCP Server 只提供 Tools

尤其在 AI Coding 场景中，很多 MCP Server 优先提供 Tools，常见原因如下。

### 1. Tools 的客户端兼容性更好

Tools 的调用流程比较统一：

```text
模型发现 Tool
→ 模型生成参数
→ 客户端执行调用
→ Server 返回结果
→ 模型继续处理
```

Resources 则需要客户端完成资源展示、选择、读取、截断和上下文注入。不同 MCP Client 对这些功能的支持程度和交互方式可能不同。

### 2. Tools 更符合 Agent 的主动执行方式

模型可以根据用户需求，主动选择 Tool 并填写参数。例如：

```js
search_specs((feature = "document-search"), (section = "requirements"));
```

如果改成 Resource Template，客户端还需要支持模板发现、URI 展开和内容加载，完整链路更依赖客户端实现。

### 3. 很多外部系统提供的是操作

GitHub、Jira、Slack、数据库、浏览器和 CI/CD 系统的常见能力包括：

- 创建或更新任务。
- 查询记录。
- 执行 SQL。
- 发送消息。
- 修改文件。
- 审批工作流。

这些能力都有明确的输入和执行结果，天然适合封装成 Tools。

### 4. Tools 更容易精确控制返回内容

Resource 可能是一份很大的文件或完整知识库内容。如果客户端直接把大量资源加入上下文，会增加 Token 消耗，也可能引入无关信息。

Tool 可以先根据参数进行筛选，只返回当前任务需要的数据：

```js
search_project_docs((query = "登录接口错误处理"), (limit = 5));
```

### 5. Tools 可以覆盖很多读取场景

开发者可以把读取能力统一封装成：

```js
get_document(path);
get_database_schema(table);
search_knowledge_base(query);
```

这些 Tools 已经可以把数据返回给模型，因此部分 Server 不再额外维护一套 Resources 接口。

## 什么时候应该提供 Resources

下面这些场景适合提供 Resources：

- 存在大量可以浏览和选择的文档。
- 数据拥有稳定、清晰的 URI。
- 用户需要手动选择要加入对话的上下文。
- 客户端需要预览文件、数据库结构或知识库条目。
- 同一份内容需要被多个 Tool 引用。
- 需要订阅并感知资源内容变化。

一个同时使用 Resources 和 Tools 的项目文档 MCP Server，可以这样设计：

```text
Resources:
  project://AGENTS.md
  project://architecture
  project://api-spec
  project://database-schema

Tools:
  search_project_docs(query)
  update_api_spec(content)
  run_architecture_check(scope)
```

Resources 负责提供稳定的项目上下文，Tools 负责搜索、修改和检查。两者配合使用，比强行把所有能力都放进同一种接口更清晰。

## 设计 MCP Server 时的检查点

在决定使用 Tool 还是 Resource 时，可以依次检查：

1. 这是一个需要执行的动作，还是一份可以定位的资料？
2. 是否需要模型根据当前任务主动生成参数？
3. 操作是否可能修改外部状态？
4. 数据是否有稳定 URI，是否需要被反复读取？
5. 目标 MCP Client 是否支持资源列表、模板和上下文加载？
6. 返回内容是否过大，是否应该先通过 Tool 检索和筛选？
7. 涉及写入、发送或执行命令时，是否设置了用户确认和权限边界？
