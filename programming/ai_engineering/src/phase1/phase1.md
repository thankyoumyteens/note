# 阶段一：从 Java 思维切换到 AI 原生开发

这份阶段一的详细学习路线，核心主旨就是四个字：**“破除执念”**。

作为资深 Java 后端，你习惯了严密的类型系统、层层封装的接口和绝对确定的执行路径。但在 Phase 1，你需要习惯动态语言的随性，并接受大模型“基于概率”的输出特性。

我们把阶段一拆解为 **5 个具体的实操步骤**，建议你按照顺序，每一个步骤写一个简单的 `.py` 脚本来验证。

---

### 第一步：建立 Python 原生 Web 肌肉记忆 (FastAPI + Pydantic)

不要一开始就碰 AI。先用你最熟悉的 Web 开发切入，建立对 Python 生态的安全感。

- **Java 映射**：Spring Boot (`@RestController`) + Hibernate Validator (`@Valid`) + Swagger。
- **学习重点**：
- 如何启动一个 FastAPI 服务。
- 学习 Pydantic 强大的数据校验能力（它是目前 Python AI 生态里做数据结构化的绝对核心）。

- **实战任务**：写一个单纯的 HTTP POST 接口。接收一段包含财务指标的 JSON（例如市盈率 PE、股息率 Dividend Yield），用 Pydantic 定义模型并做字段范围校验（如 `pe > 0`），如果不合法自动返回 422 错误。
- **避坑指南**：Python 没有 Maven/Gradle 那么重的工程结构，不要建一大堆 `controller`, `service`, `dao` 包。前期的测试代码，全塞在一个 `main.py` 里就行。

### 第二步：剥离框架，直击大模型 API 底层 (OpenAI 官方 SDK)

**这是最重要的一步！绝对不要一上来就用 LangChain。** LangChain 封装了太多细节，一旦报错，Java 程序员会本能地去翻源码，然后迷失在 Python 复杂的继承链里。

- **核心概念**：大模型的 API 其实就是一个带有特殊历史记录格式的 HTTP POST 请求。
- **学习重点**：
- 掌握三种核心角色：`System`（系统指令/人设）、`User`（用户提问）、`Assistant`（AI 回答）。
- 理解 Token 是怎么消耗的，以及 `temperature` 参数对输出稳定性的影响。
- 掌握流式输出（Streaming）的底层原生写法。

- **实战任务**：完全不用 LangChain，直接 `pip install openai`。写一个 Python 脚本，向模型提问：“请详细解释一下博格公式（Bogle's Equation）在指数投资中的应用”，并在控制台用流式打印出来。尝试修改 System Prompt，让它“以一个尖酸刻薄的华尔街交易员口吻”来回答，体会 Prompt 对大模型行为的绝对控制力。

### 第三步：掌握 Prompt Engineering (你的“新版业务逻辑”)

在传统后端，你的业务逻辑是用 `if/else`、`for` 循环和策略模式写出来的；在 AI 原生应用中，大量的业务流转是通过**提示词工程**来实现的。

- **核心技巧**：
- **Few-Shot (少样本提示)**：大模型是“按例办事”的高手。不要只给指令，要给例子。
- **CoT (思维链)**：遇到复杂的推理逻辑，在 Prompt 里加上“请一步一步思考（Think step by step）”，能显著降低模型的逻辑错误率。

- **实战任务**：写一个强大的 Prompt，实现“信息抽取”。输入一段冗长杂乱的关于 Palantir (PLTR) 或其他公司的市场新闻，让模型从中精准提取出：公司名称、事件主体、对财报的潜在影响，并**严格要求其以 JSON 格式输出**。在 Prompt 里给它提供 1-2 个标准的输入输出示例（Few-Shot）。

### 第四步：引入 LangChain 与 LCEL (AI 逻辑的“管道化”编排)

经过前面三步，你已经懂了底层原理，这时候你会发现直接用原生的 OpenAI SDK 拼接字符串太丑陋了。现在，是时候引入 LangChain 这个“编排框架”了。

- **Java 映射**：相当于从手写 JDBC 进化到了 MyBatis，从手写 Thread 进化到了 Spring Integration 的消息管道。
- **学习重点**：
- `ChatPromptTemplate`：优雅地管理带有变量的提示词。
- `OutputParsers`：把大模型输出的非结构化字符串，强制解析成你的 Pydantic 对象。
- **LCEL (LangChain 表达式语言)**：理解 `chain = prompt | model | parser` 这种类似 Unix 管道的语法糖。

- **实战任务**：使用 LCEL 重写第三步的“信息抽取”任务。体验如何通过 `|` 符号，将输入变量丝滑地流入 Prompt 模板，传给大模型，最后流经 Parser 直接变成一个可以直接操作的 Python 对象。

### 第五步：攻克上下文管理 (打破“无状态”诅咒)

大模型 API 是绝对无状态的（Stateless），它记不住上一秒你说过的话。

- **Java 映射**：这不像后端的 `HttpSession` 存在服务器内存或 Redis 里。你需要每次在请求时，把整个“聊天记录数组”完整地传过去（类似每次 HTTP 请求把所有的 Cookie 历史全带上）。
- **学习重点**：
- 理解上下文窗口（Context Window）的限制和 Token 成本。
- 学习 LangChain 的 `ChatMessageHistory`。

- **实战任务**：写一个终端里的连续对话脚本。第一回合问：“TSLA 目前的股价数据可能不准，你能告诉我处理这种脏数据的常规工程手段吗？”第二回合问：“那么在这个过程中，Redis 可以用来做什么？”观察模型是否能理解第二句话中的“这个过程”是指什么。

---

### 阶段一通关验收标准：

当你能**不看文档，手敲出一个 FastAPI 接口，接口里用 LCEL 组装了一个带有 Prompt 模板的链，并能将用户的请求转化为结构化的 JSON 返回**时，你的第一阶段就彻底圆满了。这意味着你已经建立起了 AI Native 开发的工程骨架。

在这个详细的五个步骤中，哪一步让你觉得最符合你现在的痛点，或者最想立刻打开 IDE 写几行代码验证一下？我可以为你提供该步骤的骨架代码。
