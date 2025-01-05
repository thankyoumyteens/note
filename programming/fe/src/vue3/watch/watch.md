# watch

watch 函数的第一个参数是要监听的对象。取值类型是以下几种:

- 一个函数, 返回一个值
- 一个 ref
- 一个响应式对象(reactive)
- 由以上类型的值组成的数组

## 监听 ref 对象

```html
<script lang="ts" setup>
  import { ref, watch } from "vue";

  let student = ref({
    name: "Tom",
    age: 18,
  });

  let studentInfo = ref("");

  watch(
    student,
    (newVal, oldVal) => {
      studentInfo.value = `Name: ${newVal.name}, Age: ${newVal.age}`;
    },
    {
      deep: true, // 如果要在对象内部的字段变化时触发, 需要加上这行
      immediate: true, // 数据初始化时立即执行
    }
  );

  function changeName() {
    student.value.name = "Jerry";
  }
</script>

<template>
  <div>
    <h1>{{ studentInfo }}</h1>
    <button @click="changeName">Change</button>
  </div>
</template>

<style scoped></style>
```

## 监听 reactive 对象

```html
<script lang="ts" setup>
  import { reactive, watch } from "vue";

  let student = reactive({
    name: "Tom",
    age: 18,
  });

  watch(student, (newVal, oldVal) => {
    console.log("student changed", newVal, oldVal);
  }); // 不需要加 deep: true 对象内部的字段变化就可以触发

  function changeName() {
    student.name = "Jerry";
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

## 监听 reactive 对象里的某个字段

```html
<script lang="ts" setup>
  import { reactive, watch } from "vue";

  let student = reactive({
    name: "Tom",
    age: 18,
  });

  watch(
    () => student.name, // 要写成函数形式
    (newVal, oldVal) => {
      console.log("student name changed", newVal, oldVal);
    }
  );

  function changeName() {
    student.name = "Jerry";
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

## 监听多个数据

```html
<script lang="ts" setup>
  import { reactive, watch } from "vue";

  let student = reactive({
    name: "Tom",
    age: 18,
  });

  watch(
    //[student.name, student.age], // ref对象的写法, 不需要用函数
    [() => student.name, () => student.age], // 把要监听的多个数据合并成一个数组
    (newVal, oldVal) => {
      // 此时newVal和oldVal都是包含name和age值的数组
      console.log("student name or age changed", newVal, oldVal);
    }
  );

  function changeName() {
    student.name = "Jerry";
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
