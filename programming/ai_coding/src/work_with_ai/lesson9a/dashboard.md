# 启动 Dashboard

官方 README 展示它有实时 Web Dashboard，用来查看 specs、任务和进度。

在项目目录运行：

```bash
# 默认监听 5000 端口
# 但是 macOS 系统的 Control Center，也在监听 *:5000
# 所以改用 5001
npx -y @pimzino/spec-workflow-mcp@latest . --dashboard --port 5001
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
