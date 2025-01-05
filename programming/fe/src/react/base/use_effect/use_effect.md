# useEffect

useEffect 是 React Hook 函数。它让你可以在函数组件中执行副作用操作。在类组件中, 这些操作通常放在生命周期方法中完成, 比如 componentDidMount、componentDidUpdate 和 componentWillUnmount。而在函数组件中, 你可以使用 useEffect 来实现类似的功能。

用法

```jsx
import { useEffect } from "react";

// 第一个参数称为 副作用
// 第二个参数称为依赖项
useEffect(() => {}, []);
```

不同的依赖项

- 不传: 在组件渲染完毕后, 和每次组件更新时, 都会调用副作用函数
- 传空数组: 在组件渲染完毕后, 调用副作用函数
- 传指定的 state: 在组件渲染完毕后, 和传入的 state 修改后, 都会调用副作用函数

注意: 每次触发调用两次副作用函数的话, 需要把 index.js 中的 `React.StrictMode` 标签去掉。
