# keep-alive

被keep-alive包裹的组件在组件切换过程中将状态保留在内存中, 防止重复渲染DOM, 减少加载时间及性能消耗。

keep-alive的属性: 
    
- include - 字符串或正则表达式。只有名称匹配的组件会被缓存
- exclude - 字符串或正则表达式。任何名称匹配的组件都不会被缓存
- max - 数字。最多可以缓存多少组件实例

# 生命周期函数

被包含在 keep-alive 中创建的组件, 会多出两个生命周期的钩子: activated 与 deactivated

## activated

在 keep-alive 组件激活时(切换到被包裹的组件)调用, 该钩子函数在服务器端渲染期间不被调用

## deactivated

在 keep-alive 组件停用时(切换到其他组件)调用, 该钩子在服务器端渲染期间不被调用

# include和exclude

```html
// 指定home组件和about组件被缓存
<keep-alive include="home,about" >
    <router-view></router-view>
</keep-alive>

// 除了home组件和about组件别的都缓存, 本例中就是只缓存detail组件
<keep-alive exclude="home,about" >
    <router-view></router-view>
</keep-alive>

// include和exclude的属性值是组件的名称, 也就是组件的name属性值
<script>
    export default {
      name: "home"
    };
</script>
```
