# 安装Vue Router

```
npm install vue-router
```

# 创建一个router.js文件

```javascript
import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

// 定义路由和组件的映射关系
const routes = [
  {
    // 路径
    path: '/home',
    // 路由名称
    name: 'home',
    // 对应的组件(懒加载，在该路由被访问时才会加载对应的组件)
    component: () => import('./views/Home.vue')
  },
  // 其他页面的路由
];
// 创建一个Vue Router实例，并将路由配置传递给它
const router = new VueRouter({
  routes
});
// 导出
export default router;
```

# 在Vue应用的main.js中，将Vue Router实例作为router选项传递给Vue实例

```javascript
import router from './router';
// ...
new Vue({
  router,
  render: h => h(App)
}).$mount('#app');
```

# 在Vue组件中使用路由

```html
<template>
  <div>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
    <router-link to="/contact">Contact</router-link>
    <!-- 渲染路由指定的页面 -->
    <router-view></router-view>
  </div>
</template>
```
