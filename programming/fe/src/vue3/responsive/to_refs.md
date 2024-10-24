# toRefs

从 reactive 结构赋值出来的变量不是响应式的:

```html
<script lang="ts" setup>
  import { reactive } from "vue";

  let student = reactive({
    name: "Tom",
    age: 18,
  });

  // 解构 student 对象
  // name 和 age 不是响应式的
  let { name, age } = student;

  function changeName() {
    // 不会触发视图更新
    name = "Jerry";
  }
</script>

<template>
  <div>
    <h1>{{ student.name }}</h1>
    <button @click="changeName">Change</button>
  </div>
</template>

<style scoped></style>
```

使用 toRefs 把解构出来的变量也变成响应式的:

```html
<script lang="ts" setup>
  import { reactive, toRefs } from "vue";

  let student = reactive({
    name: "Tom",
    age: 18,
  });

  // 使用 toRefs 解构 student 对象
  // name 和 age 变成了ref对象, 是响应式的
  let { name, age } = toRefs(student);

  function changeName() {
    // 触发视图更新
    // 并且更改name的值, student.name也会改变
    name.value = "Jerry";
  }
</script>

<template>
  <div>
    <h1>{{ student.name }}</h1>
    <button @click="changeName">Change</button>
  </div>
</template>

<style scoped></style>
```
