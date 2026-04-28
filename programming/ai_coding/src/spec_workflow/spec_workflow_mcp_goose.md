# Goose 配置 spec-workflow-mcp

### 1. 在终端运行这个命令，找到 npx 的真实路径：

```sh
which npx
```

### 2. 打开 goose configure 主菜单

```sh
goose configure
```

1. 用方向键选择 `● Add Extension`。
2. 类型选择 `Command-line`。
3. Name: `spec-workflow`
4. Command: `/换成你的绝对路径/npx -y @pimzino/spec-workflow-mcp@latest .`。

### 3. 重新启动 Goose

```sh
goose session
```

### 4. 验证是否安装成功

对ai说

```
请列出你当前可用的所有外部工具（Tools），看看有没有包含 spec-workflow 相关的函数。
```
