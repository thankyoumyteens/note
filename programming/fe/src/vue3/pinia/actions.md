# actions

1. 定义 actions

```ts
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state() {
    return {
      name: "张三",
      age: 18,
    };
  },
  actions: {
    // 定义action
    changeName(name: string) {
      this.name = name;
    },
  },
});
```

2. 调用 actions

```ts
import { useUserStore } from "./store/user";
// 通过useUserStore获取userStore
const userStore = useUserStore();

// 使用actions修改userStore中的name
const change = () => {
  userStore.changeName("new name");
};
```
