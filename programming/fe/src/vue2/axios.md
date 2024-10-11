# 集成 axios

1. 安装

```sh
npm install axios --save
```

2. 新建 request.js

```js
import axios from "axios";

const request = axios.create({
  // 后端地址
  baseURL: "http://localhost:27431",
  timeout: 3000,
});

export default request;
```

3. 导出接口

```js
import request from "@/utils/request";

export function getMenuList() {
  return request({
    url: "/menu/list",
    method: "get",
  });
}
```

3. 使用

```vue
<template>
  <div></div>
</template>

<script>
import { getMenuList } from "@/api/menu";

export default {
  methods: {
    initMenu() {
      getMenuList().then((res) => {
        console.log(res);
      });
    },
  },
};
</script>

<style></style>
```
