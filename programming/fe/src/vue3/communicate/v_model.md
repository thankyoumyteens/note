# v-model

element plus 把 element-ui 中的 `:xxx.sync` 换成了 `v-model`

```html
<el-dialog
  v-model="dialogVisible"
  title="Tips"
  width="500"
  :before-close="handleClose"
></el-dialog>

<el-dialog
  title="提示"
  :visible.sync="dialogVisible"
  width="30%"
  :before-close="handleClose"
>
</el-dialog>
```

## 子组件实现 v-model

v-model 默认只能写在 html 表单标签上。子组件要支持 v-model 需要满足两个条件:

1. props 中定义一个值 `modelValue`
2. emit 中定义一个 `update:modelValue` 事件

实现:

1. 子组件

```html
<script lang="ts" setup>
  const { modelValue } = defineProps({
    modelValue: String,
  });
  const updateEvent = defineEmits(["update:modelValue"]);
</script>

<template>
  <div>
    <input
      type="text"
      :value="modelValue"
      @input="
        updateEvent(
          'update:modelValue',
          (<HTMLInputElement>$event.target).value
        )
      "
    />
  </div>
</template>

<style scoped></style>
```

2. 父组件

```html
<script lang="ts" setup>
  import { ref, watch } from "vue";
  import Child from "./Child.vue";
  const val1 = ref("");
  watch(val1, (newVal) => {
    console.log("val1 changed to: ", newVal);
  });
</script>

<template>
  <div>
    <Child v-model="val1" />
  </div>
</template>

<style scoped></style>
```

## 不使用 modelValue 实现 v-model

不使用 modelValue 实现 v-model 在使用时需要用这种格式: `v-model:自定义名称="变量"`

1. 子组件

```html
<script lang="ts" setup>
  // 把modelValue换成自定义名称inputValue
  const { inputValue } = defineProps({
    inputValue: String,
  });
  const updateEvent = defineEmits(["update:inputValue"]);
</script>

<template>
  <div>
    <input
      type="text"
      :value="inputValue"
      @input="
        updateEvent(
          'update:inputValue',
          (<HTMLInputElement>$event.target).value
        )
      "
    />
  </div>
</template>

<style scoped></style>
```

2. 父组件

```html
<script lang="ts" setup>
  import { ref, watch } from "vue";
  import Child from "./Child.vue";
  const val1 = ref("");
  watch(val1, (newVal) => {
    console.log("val1 changed to: ", newVal);
  });
</script>

<template>
  <div>
    <!-- 使用时的变化 -->
    <Child v-model:inputValue="val1" />
  </div>
</template>

<style scoped></style>
```
