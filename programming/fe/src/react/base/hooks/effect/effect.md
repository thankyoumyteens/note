# useEffect

`useEffect` 用于处理函数组件中的副作用(side effects)。副作用是指那些在组件渲染之外发生的操作，例如数据获取、订阅、手动更改 DOM 等。`useEffect` 类似于类组件中的 `componentDidMount`、`componentDidUpdate` 和 `componentWillUnmount` 生命周期方法。

主要用途：

1. 数据获取：在组件挂载或更新时从服务器获取数据
2. 订阅事件：监听某些事件并在事件触发时执行特定操作
3. 手动更改 DOM：直接操作 DOM 元素
4. 清理操作：在组件卸载或更新前执行清理操作，例如取消订阅或清除定时器

基本语法：

```javascript
useEffect(effect, dependencies);
```

- effect：一个函数，包含需要执行的副作用操作
- dependencies：一个数组，包含所有 `effect` 函数中使用的变量。如果这些变量发生变化，`effect` 函数将重新执行。如果传递一个空数组 `[]`，则 `effect` 只会在组件挂载时执行

## 组件挂载时调用

```jsx
import { useEffect } from "react";

function App() {
  // 如果你的应用使用了React的StrictMode，React会在开发模式下故意多次调用useEffect方法，
  // 这是为了帮助你发现一些常见的问题，例如数据获取或订阅的重复调用。
  // 所以在开发模式下，useEffect会被调用两次，但在生产模式下只会调用一次。
  useEffect(() => {
    console.log("组件挂载");
  }, []);
  return <div></div>;
}

export default App;
```

## 监听 state 的变化

```jsx
import { useEffect, useState } from "react";

function App() {
  const [count, setCount] = useState(0);
  // 数组中传入count，只有count的值发生变化时，才会执行useEffect中的回调函数
  useEffect(() => {
    console.log("count的值发生了变化", count);
  }, [count]);
  return (
    <div>
      <h1>{count}</h1>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}

export default App;
```

## 组件卸载时调用

```jsx
function ChildComponent() {
  useEffect(() => {
    // 组件挂载完毕后启动定时器
    const timer = setInterval(() => {
      console.log("running");
    }, 1000);

    // 组件卸载时会执行return返回的函数
    return () => {
      // 组件卸载前清理定时器
      clearInterval(timer);
    };
  }, []);
  return <div>子组件</div>;
}
```
