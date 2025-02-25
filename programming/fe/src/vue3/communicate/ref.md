# 通过 ref

父组件通过 ref 获取子组件的属性或方法

### 1. 子组件指定可以被外部访问的数据

```html
<script setup lang="ts">
  const getMsg = () => {
    return "来自子组件的消息";
  };

  // 指定可以被外部访问的数据
  defineExpose({
    getMsg,
  });
</script>

<template>
  <div>子组件</div>
</template>
```

### 2. 父组件调用子组件的函数

```html
<script setup lang="ts">
  import { ref } from "vue";
  import ChildComponent from "./components/ChildComponent.vue";

  // 定义子组件的类型
  type ChildComponentType = InstanceType<typeof ChildComponent>;

  const childRef = ref<ChildComponentType>(null);

  const callChildFn = () => {
    // 调用子组件的函数
    const msg = childRef.value.getMsg();
    console.log(msg);
  };
</script>

<template>
  <div>
    <!-- 把childRef绑定到子组件 -->
    <ChildComponent ref="childRef" />
    <button @click="callChildFn">调用子组件的函数</button>
  </div>
</template>
```
