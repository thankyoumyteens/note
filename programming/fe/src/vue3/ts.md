# 使用 ts

ts:

```ts
export interface Demo {
  name: string;
  age: number;
}
```

vue:

```vue
<script lang="ts" setup>
// ts接口前面需要加 type
import { type Demo } from "@/types/demo";

const student: Demo = {
  name: "Tom",
  age: 18,
};
</script>

<template>
  <div>ok</div>
</template>

<style scoped></style>
```
