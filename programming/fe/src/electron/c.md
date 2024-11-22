# 与主进程通信

在 Electron 中，进程使用 ipcMain 和 ipcRenderer 模块，通过开发人员定义的“通道”传递消息来进行通信。双向 IPC 的一个常见应用是从渲染器进程代码调用主进程模块并等待结果。 这可以通过将 ipcRenderer.invoke 与 ipcMain.handle 搭配使用来完成。

### 1. 在预处理脚本中绑定事件并暴露出去

```js
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("server", {
  chooseFile: (options) => ipcRenderer.invoke("chooseFile", options),
});
```

### 2. 主进程监听事件

```js
const { app, BrowserWindow, ipcMain, dialog } = require("electron/main");
const path = require("node:path");

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      // 将预处理脚本附在渲染进程上
      preload: path.join(__dirname, "preload.js"),
    },
  });

  win.loadFile("index.html");
};

// 选择文件
async function handleFileOpen(options) {
  const { canceled, filePaths } = await dialog.showOpenDialog(options);
  if (!canceled) {
    return filePaths[0];
  }
}

app.whenReady().then(() => {
  // 监听事件
  ipcMain.handle("chooseFile", (event, options) => handleFileOpen(options));
  createWindow();
});
```

### 3. 在页面中调用

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <button id="btn">选择文件</button>
    <p id="result"></p>
  </body>
  <script>
    document.getElementById("btn").addEventListener("click", async () => {
      // 调用主进程的方法
      const filePath = await server.chooseFile({
        message: "请选择文件", // 选择文件对话框的标题(mac系统有效)
      });
      document.getElementById("result").innerHTML = filePath;
    });
  </script>
</html>
```
