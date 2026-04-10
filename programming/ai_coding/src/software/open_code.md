# 安装 OpenCode

OpenCode 是一款 Go 语言编写的轻量级工具。在 macOS 系统上，你可以直接打开终端并执行以下脚本进行安装：

```sh
curl -fsSL https://opencode.ai/install | bash
```

安装完成后，通过 cd 命令进入你想要修改或分析的代码项目目录，然后直接输入以下命令即可唤醒 AI：

```sh
opencode
```

## 接入大模型

启动后的第一件事是告诉 OpenCode 它该用什么“大脑”来思考。在对话框中输入核心指令：

```sh
/connect
```

系统会弹出一个支持 75+ 供应商的列表。

选择 OpenRouter。系统会提示你输入 OpenRouter 的 API Key（以 `sk-or-v1-` 开头）。完成后，OpenCode 会自动在配置文件中生成对应的结构。

## 切换模型

如果你已经进入了 OpenCode 的终端交互界面，并且想在不丢失当前代码上下文的情况下更换模型，请直接在输入框中键入：

```sh
/models
```

按下回车后，界面会弹出一个模型选择对话框，按字母顺序列出所有已配置提供商（如 GitHub Copilot、OpenAI、Ollama 等）的可用模型。通过键盘上下方向键选中你需要的模型即可立刻完成切换。
