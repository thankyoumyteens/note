# 使用 Element Plus

1. 安装

```sh
cd frontend
npm install element-plus
```

2. 修改 main.js

```js
import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import App from "./App.vue";
import "./style.css";

const app = createApp(App);
app.use(ElementPlus);
app.mount("#app");
```

3. 使用

```html
<el-button type="primary" @click="greet">Greet</el-button>
```

4. 运行

```sh
wails dev
```
