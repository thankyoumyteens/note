# useCallback

`useCallback` 可以缓存一个函数的引用, 只有在依赖项发生变化时才会返回一个新的函数引用

主要用途：

1. 性能优化：避免在每次渲染时创建新的函数引用, 特别是当这些函数作为 props 传递给子组件时, 可以防止不必要的子组件重新渲染
2. 保持函数引用的一致性：确保依赖项发生变化时才返回新的函数引用, 从而保持函数引用的一致性

基本语法：

```javascript
const memoizedCallback = useCallback(() => {
  // 函数体
}, [dependencies]);
```

- `() => { ... }`：这是一个函数, 你希望 `useCallback` 缓存其引用。
- `[dependencies]`：这是一个依赖数组, 包含所有影响函数引用的变量。如果这些变量发生变化, `useCallback` 会返回一个新的函数引用

## 基本用法

假设你有一个子组件, 它接收一个回调函数作为 prop。每次父组件重新渲染时, 都会创建一个新的回调函数, 导致子组件不必要的重新渲染。使用 `useCallback` 可以避免这种情况。

```jsx
import React, { useState, useCallback } from "react";

// 子组件
function ChildComponent({ onButtonClick }) {
  console.log("ChildComponent rendered");
  return <button onClick={onButtonClick}>Click me</button>;
}

// 父组件
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // 使用useCallback缓存handleButtonClick函数的引用
  // 只有当依赖数组中的变量发生变化时, useCallback才会返回一个新的函数引用
  // 由于依赖数组为空, handleButtonClick的引用在整个组件的生命周期内保持不变
  // 这样即使ParentComponent重新渲染, ChildComponent也不会因为接收到新的onButtonClick函数引用而重新渲染
  const handleButtonClick = useCallback(() => {
    setCount((prevCount) => prevCount + 1);
  }, []);
  return (
    <div>
      <ChildComponent onButtonClick={handleButtonClick} />
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <p>Count: {count}</p>
    </div>
  );
}

export default ParentComponent;
```

## useCallback 与 useMemo 的区别

- useCallback：用于记忆化函数引用, 避免不必要的函数创建
- useMemo：用于记忆化计算结果, 避免不必要的计算
