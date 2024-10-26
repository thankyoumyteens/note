# getters

1. 定义 getters

```ts
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state() {
    return {
      name: "张三",
      age: 18,
    };
  },
  getters: {
    // 定义getter
    getName(state): string {
      return state.name + "!";
    },
  },
});
```

2. 使用 getters

```ts
import { useUserStore } from "./store/user";
import { storeToRefs } from "pinia";
const userStore = useUserStore();
const { getName } = storeToRefs(userStore);

// getName是computed属性，可以直接获取值
console.log(getName.value);
```
