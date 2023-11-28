# 虚拟DOM

1. 本质是Object类型的对象。
2. 虚拟DOM比较“轻”, 真实DOM比较“重”, 因为虚拟DOM是React内部在用, 无需真实DOM上那么多的属性。
3. 虚拟DOM最终会被React转化为真实DOM, 呈现在页面上。

# 使用jsx创建虚拟DOM

```jsx
//1.创建虚拟DOM
const VDOM = ( /* 此处一定不要写引号, 因为不是字符串 */
    <h1 id="title">
    <span>Hello,React</span>
    </h1>
)
//2.渲染虚拟DOM到页面
ReactDOM.render(VDOM,document.getElementById('test'))
```

# 使用js创建虚拟DOM

```jsx
//1.创建虚拟DOM
const VDOM = React.createElement('h1', {id:'title'}, React.createElement('span', {}, 'Hello,React'))
//2.渲染虚拟DOM到页面
ReactDOM.render(VDOM,document.getElementById('test'))
```
