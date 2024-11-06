# useRef

`useRef` 可以帮助你在函数组件中处理各种需要持久化存储和 DOM 操作的场景。通过 `useRef`，你可以避免不必要的重新渲染，并且能够方便地访问和操作 DOM 元素。

主要用途：

1. 持久存储: `useRef` 可以用来存储任何可以在整个组件生命周期内持久化的数据，而不需要触发组件的重新渲染
2. DOM 访问: 你可以使用 `useRef` 来获取对 DOM 元素的直接引用，类似于类组件中的 `ref` 属性
3. 跨渲染保持数据: `useRef` 可以用来保存上一次渲染的数据，这对于某些需要跨渲染保持状态的场景非常有用

`useRef` 返回一个对象，该对象有一个 `.current` 属性。你可以在 `.current` 上存储任何值，包括原始值、对象、函数等。

## DOM 访问

```jsx
import { useRef, useState } from "react";

function App() {
  // 创建一个ref对象, 用于绑定到input标签上
  const inputRef = useRef(null);
  // 通过inputRef.current获取input标签的DOM对象
  // 然后调用input标签的focus方法，使input标签获取焦点
  const focusInput = () => inputRef.current.focus();
  return (
    <div>
      {/* 通过ref属性将inputRef与input标签关联 */}
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>获取焦点</button>
    </div>
  );
}

export default App;
```

## 记录上一次的值

```jsx
import { useRef, useState } from "react";

function App() {
  const [count, setCount] = useState(0);
  // 记录上一次的count值
  const prev = useRef();

  const increment = () => {
    prev.current = count;
    setCount(count + 1);
  };

  return (
    <div>
      <p>{count}</p>
      <button onClick={increment}>Increment</button>
      <p>上一次的值：{prev.current}</p>
    </div>
  );
}

export default App;
```
