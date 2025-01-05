# 基本使用

1. 传递的数据类型 types.ts:

```ts
export interface DataItem {
  id: number;
  name: string;
}
```

2. 父组件 Parent.vue:

```html
<script lang="ts" setup>
  import Child from "./Child.vue";
  import { reactive } from "vue";
  import { type DataItem } from "./types";

  let dataList = reactive<DataItem[]>([
    { id: 1, name: "John" },
    { id: 2, name: "Doe" },
    { id: 3, name: "Jane" },
  ]);
</script>

<template>
  <div>
    <!-- 向子组件传递props -->
    <Child :dataList="dataList" />
  </div>
</template>

<style scoped></style>
```

3. 子组件 Child.vue:

```html
<script lang="ts" setup>
  import { type DataItem } from "./types";

  // 要接收的props的类型定义
  interface Props {
    dataList: DataItem[];
    otherProp?: string; // 可选的props
  }

  // 通过defineProps接收props
  // defineProps<Props>()返回一个对象, 包含了所有props的值
  let { dataList } = defineProps<Props>();

  // 不限制类型的简写方式
  // let { dataList, otherProp } = defineProps(["dataList", "otherProp"]);
</script>

<template>
  <div>
    <ul>
      <!-- 使用props中的dataList -->
      <li v-for="item in dataList" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<style scoped></style>
```
