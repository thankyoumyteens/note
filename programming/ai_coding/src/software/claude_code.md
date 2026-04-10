# 安装 Claude Code

```sh
# 下面两种方法任选其一
npm install -g @anthropic-ai/claude-code
curl -fsSL https://claude.ai/install.sh | bash
```

安装 CC Switch

```sh
brew tap farion1231/ccswitch
brew install --cask cc-switch
# 更新：
brew upgrade --cask cc-switch
```

## 接入大模型

1. 打开 CC Switch
2. 添加供应商：点击"添加供应商" → 选择预设或创建自定义配置
3. 切换供应商：
   - 主界面：选择供应商 → 点击"启用"
   - 系统托盘：直接点击供应商名称（立即生效）
4. 生效方式：重启终端或对应的 CLI 工具以应用更改（CLaude Code 无需重启）
5. 恢复官方登录：添加"官方登录"预设，重启 CLI 工具后按照其登录/OAuth 流程操作
