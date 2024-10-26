# 创建 state

为数据创建仓库, 以 user 为例: src/store/user.ts:

```ts
import { defineStore } from "pinia";

// 定义state
export const useUserStore = defineStore("user", {
  state() {
    return {
      name: "张三",
      age: 18,
    };
  },
});
```
