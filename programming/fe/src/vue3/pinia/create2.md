# 使用组合式 API 创建 state

```ts
import { defineStore } from "pinia";
import { ref } from "vue";

// 定义state
export const useUserStore = defineStore("user", () => {
  let name = ref("张三");
  let age = ref(18);
  // 定义getter
  const getName = (): string => {
    return name.value + "!";
  };
  // 定义action
  const changeName = (newName: string) => {
    name.value = newName;
  };
  return {
    name,
    age,
    getName,
    changeName,
  };
});
```
