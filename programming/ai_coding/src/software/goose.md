# 安装 Goose

### 1. 安装

```sh
brew install block-goose-cli
```

### 2. 配置模型

```sh
goose configure
```

1. 在你当前的界面，直接按回车选择 `● Configure Providers`。
2. 在接下来的提供商列表里，用上下键找到并选择 `OpenRouter`。
3. 它会问你是否要把 API Key 保存到系统钥匙串（keyring），选 Yes。
4. 粘贴你 OpenRouter 的 API Key： `sk-or-v1-...`（注意：输入时屏幕上通常不会显示字符，这是正常的保护机制，贴完直接回车）。
   - 如果它检测到你之前的终端环境（`~/.zshrc`）里已经配置过 `OPENROUTER_API_KEY` 了，就会直接读取那个现成的值。
5. 当它要求输入 `Model` 时，填入：`deepseek/deepseek-chat`。
6. 配置完成后，它通常会提示配置成功。

### 3. 重新启动 Goose

```sh
goose session
```
