# 安装 Aider

因为 Aider 是纯 Python 开发的终端工具，在 macOS 环境下配置起来非常丝滑。

### 1. 安装 Aider

```bash
brew install aider
aider --version
```

### 2. 配置 API 密钥

为了方便随时切换模型且不用每次都输入密码，最优雅的方式是将 API Key 写入你的终端配置文件中。请编辑你的 `~/.zshrc` 环境变量文件：

```bash
# 接入 OpenRouter
export OPENROUTER_API_KEY="sk-or-v1-..."
```

保存后，运行 `source ~/.zshrc` 使其立即生效。

## 启动与模型切换

在你的项目目录下（确保该目录已经运行过 `git init` 初始化了仓库），你可以通过不同的参数启动 Aider。

**日常轻量级开发（使用 DeepSeek，速度快且成本极低）：**

```bash
# 注意前缀 openrouter/
aider --model openrouter/deepseek/deepseek-chat
```

**核心架构重构或复杂 Bug（使用 Claude 4.6 Sonnet）：**

```bash
export http_proxy=http://127.0.0.1:6152
export https_proxy=http://127.0.0.1:6152
aider --model openrouter/anthropic/claude-4.6-sonnet
```

## 必会的 5 个核心命令 (Aider 的灵魂)

进入 Aider 的交互式终端后，你会经常用到以下几个斜杠命令：

- **/add <文件名>**：把文件加入 Aider 的上下文。**注意：必须 add 之后，AI 才能修改该文件。** 可以使用通配符，比如 `/add src/*.py`。
- **/drop <文件名>**：把文件移出上下文。这非常重要，不仅能节省 Token，更能防止 AI 产生幻觉去乱改不相关的代码。
- **/model <模型名>**：在会话中途无缝切换模型。比如聊着聊着发现 DeepSeek 搞不定复杂的微服务逻辑，直接输入 `/model claude-3-5-sonnet-20241022` 让它接手。
- **/undo**：撤销 AI 的上一次代码修改和 Git 提交。这是最能提升安全感的命令，大胆让 AI 试错，改坏了一键回退。
- **/ask <问题>**：单纯向 AI 提问或解释代码，明确告诉 AI **不要**执行任何代码修改。

## 推荐的高效工作流

**步骤一：精准投喂上下文**
永远只把相关的代码文件 `/add` 进去。例如，如果你在重构一个后端的数据库查询方法，只加入对应的 Repository 接口和具体的实现类，不要把整个项目的配置和路由文件全加进去。Aider 会通过底层的 Repo Map 自动感知未添加文件中的类名和签名，不用担心它完全瞎眼。

**步骤二：先描述意图，再让它动手**
遇到大需求，先用 `/ask` 讨论思路：“我想在这里加一个 Redis 缓存层，你觉得应该改动哪几个文件？” 确定好计划后，把遗漏的文件 `/add` 进来，再下达正式指令。

**步骤三：检查 Commit**
Aider 修改完成后，会自动用英文写一段标准的 Git Commit。你可以通过 `git log` 快速扫一眼，确认它的修改逻辑是否符合你的预期。

你的项目目前是全新的，还是已经有一定规模的旧代码库？（这会决定你在 Aider 中是否需要配置一些进阶的 Lint/Test 自动化校验命令）
