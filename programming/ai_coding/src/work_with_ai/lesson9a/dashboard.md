# 启动 Dashboard

官方 README 展示它有实时 Web Dashboard，用来查看 specs、任务和进度。

在项目目录运行：

```bash
npx -y @pimzino/spec-workflow-mcp@latest . --dashboard
```

或者如果官方版本要求 project path 在最后，就按它的 README 调整为：

```bash
npx -y @pimzino/spec-workflow-mcp@latest /path/to/ai-doc-summary --dashboard
```

如果启动成功，通常会提示 Dashboard 地址。你只在本机浏览器打开即可。

安全边界：

```text
不要把 Dashboard 暴露到公网
不要配置反向代理到公网
不要把 secret / token 写进 spec
不要把敏感信息写进 approval / task logs
```

Dashboard 的价值是看：

```text
1. 当前有哪些 specs
2. 每个 spec 处于哪个阶段
3. requirements / design / tasks 是否审批
4. tasks 完成进度
5. implementation logs
```
