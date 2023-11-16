# 通过 js 调用自定义弹窗组件

1. 定义弹窗组件：

```html
<template>
  <el-dialog
    :visible.sync="visible"
    :title="title"
    modal="true"
    :custom-class="size"
    modal-append-to-body="true"
    append-to-body="true"
    lock-scroll="true"
    show-close="true"
    destroy-on-close="true"
  >
    <div class="notify-container">
      <div class="notify-icon icon-warning"></div>
      <div class="notify-content">{{ content }}</div>
    </div>
    <template v-slot:footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button @click="handleConfirm" type="primary">确定</el-button>
    </template>
  </el-dialog>
</template>

<script>
  export default {
    name: "MyNotifyDialog",
    data() {
      return {
        visible: false,
        title: "提示",
        size: "small",
        content: "",
        confirmCallback: () => {},
        cancelCallback: () => {},
      };
    },
    methods: {
      show(conf) {
        this.visible = true;
        if (conf["title"]) {
          this.title = conf["title"];
        }
        if (conf["content"]) {
          this.content = conf["content"];
        }
        if (conf["confirmCallback"]) {
          this.confirmCallback = conf["confirmCallback"];
        }
        if (conf["cancelCallback"]) {
          this.cancelCallback = conf["cancelCallback"];
        }
      },
      handleConfirm() {
        this.confirmCallback();
        this.visible = false;
      },
      handleCancel() {
        this.cancelCallback();
        this.visible = false;
      },
    },
  };
</script>

<style lang="scss" scoped>
  .notify-container {
    width: 100%;
    height: 100%;
    position: relative;
    .notify-icon {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #f69d3d;
      font-size: 24px !important;
    }
    .notify-content {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, 100%);
    }
  }
</style>
```

2. 在 main.js 中引入：

```js
import MyNotifyDialog from "@/components/MyNotifyDialog/index.vue";
const constructor = Vue.extend(MyNotifyDialog);
const notifyInstance = new constructor();
notifyInstance.$mount();
document.body.appendChild(notifyInstance.$el);
Vue.prototype.$myNotify = notifyInstance;
```

3. 在 vue 页面中使用：

```html
<template>
  <div>
    <!-- ... -->
  </div>
</template>

<script>
  export default {
    data() {
      return {
        // ...
      };
    },
    methods: {
      del() {
        this.$myNotify.show({
          title: "删除",
          content: "是否确定删除？",
          confirmCallback: () => {
            doDelete({
              id: this.delId,
            }).then((res) => {
              if (res.data.status === 0) {
                this.$message("删除成功");
                this.refreshData();
              } else {
                this.$message("删除失败");
              }
            });
          },
        });
      },
    },
  };
</script>

<style lang="scss" scoped></style>
```
