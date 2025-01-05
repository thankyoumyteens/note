# props 默认值

在 3.5 及高版本, 使用响应式 Props 解构解

```ts
let { dataList = [], otherProp = "" } = defineProps<Props>();
```

在 3.4 及更低版本, 使用 withDefaults

```ts
import { withDefaults } from "vue";

let { dataList, otherProp } = withDefaults(defineProps<Props>(), {
  dataList: () => [],
  otherProp: "default value",
});
```
