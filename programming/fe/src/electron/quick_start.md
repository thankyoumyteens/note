# 基本使用

### 1. 创建项目

```sh
mkdir my-electron-app && cd my-electron-app
npm init
npm install electron --save-dev
```

### 2. 修改 package.json

```json
"scripts": {
    "start": "electron .",
},
```

### 3. 创建 index.html

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta
      http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'"
    />
    <meta
      http-equiv="X-Content-Security-Policy"
      content="default-src 'self'; script-src 'self'"
    />
    <title>Hello from Electron renderer!</title>
  </head>
  <body>
    <h1>Hello from Electron renderer!</h1>
    <p>👋</p>
  </body>
</html>
```

### 4. 创建 index.js

也有可能不叫 index.js, 具体看 package.json 中的 main 对应的 js 名称。

```js
const { app, BrowserWindow } = require("electron");

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  });

  win.loadFile("index.html");
};

// 在应用准备就绪时调用函数
app.whenReady().then(() => {
  createWindow();
});
```

### 5. 运行

```sh
npm run start
```
