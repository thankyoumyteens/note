# 使用 EventBus 通信

EventBus 是一种在 Vue 组件之间进行通信的机制，它允许你在一个组件中触发事件，并在另一个组件中监听这些事件。

1. 创建 event-bus.js, 创建一个新的 Vue 实例作为中央事件总线。这个实例不绑定到任何特定的组件，而是作为一个全局的事件中心

```js
import Vue from "vue";
const EventBus = new Vue();
export default EventBus;
```

2. 触发事件, 在任何组件中使用 $emit 方法来触发事件

```js
import EventBus from "./event-bus";

export default {
  methods: {
    triggerEvent() {
      EventBus.$emit("my-event", { data: "Hello EventBus" });
    },
  },
};
```

3. 监听事件, 在另一个组件中使用 $on 方法来监听事件

```js
import EventBus from "./event-bus";

export default {
  mounted() {
    EventBus.$on("my-event", (data) => {
      console.log("Received data:", data);
    });
  },
};
```

4. 取消监听事件

```js
import EventBus from "./event-bus";

export default {
  destroyed() {
    EventBus.$off("my-event");
  },
};
```
