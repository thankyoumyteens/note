# mitt

1. 安装

```sh
npm install mitt --save
```

2. 创建 src/utils/emitter.ts:

```ts
import mitt from "mitt";

const emitter = mitt();

export default emitter;
```

3. 父组件

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
  import emitter from "@/utils/emitter";

  // 绑定事件
  emitter.on("changeValue", (data) => {
    console.log(data);
  });

  // 解绑事件
  // emitter.off("changeValue");
  // 解绑所有事件
  // emitter.all.clear();
</script>

<template>
  <div>
    <Child />
  </div>
</template>

<style scoped></style>
```

4. 子组件

```html
<script lang="ts" setup>
  import emitter from "@/utils/emitter";

  const add = () => {
    // 触发事件
    emitter.emit("changeValue", "Hello World");
  };
</script>

<template>
  <div>
    <button @click="add">Add</button>
  </div>
</template>

<style scoped></style>
```
