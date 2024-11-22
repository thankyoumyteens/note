# 主进程和渲染器进程

electron 有两种类型的进程：主进程 和 渲染器进程。

## 主进程

每个 Electron 应用都有一个单一的主进程，作为应用程序的入口点。 主进程在 Node.js 环境中运行，这意味着它具有 require 模块和使用所有 Node.js API 的能力。

主进程的主要目的是使用 BrowserWindow 模块创建和管理应用程序窗口。BrowserWindow 类的每个实例创建一个应用程序窗口，且在单独的渲染器进程中加载一个网页。

```js
const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  });

  win.loadFile("index.html");
};
```

主进程还能通过 Electron 的 app 模块来控制应用程序的生命周期。

```js
app.whenReady().then(() => {
  createWindow();
});

app.on("window-all-closed", () => {
  app.quit();
});
```

## 渲染器进程

每个 Electron 应用都会为每个打开的 BrowserWindow 生成一个单独的渲染器进程。 渲染器负责渲染网页内容。渲染器无法直接访问 require 或其他 Node.js API。

## 预加载脚本

预加载脚本可以在 BrowserWindow 构造方法中的 webPreferences 选项里被附加到主进程。

```js
const win = new BrowserWindow({
  webPreferences: {
    preload: "path/to/preload.js",
  },
});
```

渲染器进程可以调用预加载脚本中暴露的 api:

```js
// preload.js
const { contextBridge } = require("electron");
contextBridge.exposeInMainWorld("myAPI", () => "ok");

// index.html
console.log(window.myAPI()); // ok
```
