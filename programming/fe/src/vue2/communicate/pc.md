# 使用 props 和事件通信

## 父组件通过 props 向子组件传值

1. 父组件发送

```html
<child-a :msg="helloMessage"></child-a>
```

2. 子组件接收

```html
<template>
  <div>{{ msg }}</div>
</template>
<script>
  export default {
    props: {
      msg: {
        type: String,
        default: "",
      },
    },
  };
</script>
```

## 子组件通过自定义事件向父组件传值

1. 子组件发送

```html
<script>
  export default {
    methods: {
      change() {
        this.$emit("changMsg", "新消息");
      },
    },
  };
</script>
```

2. 父组件接收

```html
<template>
  <child-a @changMsg="changMsg"></child-a>
</template>
<script>
  export default {
    methods: {
      changMsg(msg) {
        console.log(msg);
      },
    },
  };
</script>
```
