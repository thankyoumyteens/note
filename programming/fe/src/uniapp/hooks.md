# 页面生命周期钩子

- onLoad 监听页面加载，该钩子被调用时，响应式数据、计算属性、方法、侦听器、props、slots 已设置完成
- onShow 监听页面显示，页面每次出现在屏幕上都触发，包括从下级页面返回露出当前页面
- onReady 监听页面初次渲染完成，此时组件已挂载完成，DOM 树(`$el`)已可用，注意如果渲染速度快，会在页面进入动画完成前触发
- onHide 监听页面隐藏
- onUnload 监听页面卸载

```ts
import { onLoad, onShow, onReady, onHide, onUnload } from "@dcloudio/uni-app";

onLoad(() => {
  console.log("index onLoad");
});
onShow(() => {
  console.log("index onShow");
});
onReady(() => {
  console.log("index onReady");
});
onHide(() => {
  console.log("index onHide");
});
onUnload(() => {
  console.log("index onUnload");
});
```
