# 安装 spec-workflow-mcp

在终端中，建议将 Spec-workflow 的 MCP 服务进行全局安装，这样以后在任何新项目中都可以直接复用，而不需要每次都重新下载：

```sh
npm install -g @pimzino/spec-workflow-mcp@latest
```

## 启动 Web 仪表板

默认运行在端口 5000

```sh
# 在 mac 上 5000 端口可能会被 AirPlay 占用，所以用其它的端口启动
spec-workflow-mcp --dashboard --port 5001
```

注意： 只需要一个仪表板实例。所有项目都将连接到同一个仪表板。
