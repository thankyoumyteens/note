# 启动 Dashboard

启动 Web Dashboard，用来查看 specs、任务和进度。

在随便一个项目的根目录下运行即可，他会自动收集运行中的所有 spec 项目：

```bash
# 默认监听 5000 端口
# 但是 macOS 系统的 Control Center，也在监听 *:5000
# 所以改用 5001
npx -y @pimzino/spec-workflow-mcp@latest . --dashboard --port 5001
```

如果启动成功，通常会提示 Dashboard 地址。你只在本机浏览器打开即可。
