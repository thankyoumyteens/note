# Claude Code 配置 spec-workflow-mcp

通过配置 `.mcp.json` 文件实现。`.mcp.json` 文件可以写到两个地方：

1. 用户的主目录：提供通用的工具和环境变量
2. 特定项目的根目录：提供仅对当前项目生效的特定工具

当你运行 Claude Code 时，底层的 MCP 客户端通常会执行一套“合并逻辑”：它会先读取 主目录的全局配置 (`~/.mcp.json`) 作为底座，然后再读取 当前项目的局部配置 (`./.mcp.json`)。主目录全局配置的优先级高于当前目录。

### 写法一

前提条件： 这种写法直接把 spec-workflow-mcp 作为系统命令调用。这意味着你必须提前通过 `npm install -g spec-workflow-mcp` 将其全局安装，并且确保它的可执行文件在你的系统环境变量（`$PATH`）中，否则系统会报“找不到命令”的错误。

```json
{
  "mcpServers": {
    "spec-workflow": {
      "type": "stdio",
      "command": "spec-workflow-mcp",
      "args": ["/path/to/my-project"],
      "env": {}
    }
  }
}
```

- `type: "stdio"`：明确告诉客户端，这个 MCP Server 使用的是标准的输入输出流（Standard I/O）进行通信。通常情况下，MCP 默认就是 stdio，所以不写也可以。
- `"args": ["/path/to/my-project"]`：传给 spec-workflow-mcp 程序的启动参数，可以为空。它的作用是告诉工具：“你只能在这个 my-project 项目目录下读取规范和生成代码”。无论你在电脑的哪个目录下启动 Claude Code，Spec-workflow 都会精准对齐到这个具体的项目中。这在安全性（防止 AI 误改其他目录文件）和多项目管理上非常有用。
- `env: {}`：明确传递了一个空的环境变量对象。

注意：spec-workflow-mcp 的设计初衷是为单个特定的项目提供深度上下文隔离。它的源码在解析启动参数（args）时，通常只会抓取第一个有效的目录路径作为它的“Root Workspace（根工作区）”。如果传进去多个目录，后面的会直接被它的参数解析器丢弃或忽略。

### 写法二

```json
{
  "mcpServers": {
    "spec-workflow": {
      "command": "npx",
      "args": ["-y", "spec-workflow-mcp"]
    }
  }
}
```

核心区别：

- `"command": "npx"` 表示真正执行的命令是 npx。
- `args: ["-y", "spec-workflow-mcp"]` 是告诉 npx 去执行这个包（`-y` 是自动回答 "yes" 以跳过安装确认提示）。

优势：不需要提前全局安装。如果你从来没有用 npm 安装过这个包，npx 会在后台自动拉取最新的包并缓存在本地运行。它非常适合用来快速尝鲜，或者在换了一台新电脑时，不用关心环境有没有装好，直接就能跑起来。
