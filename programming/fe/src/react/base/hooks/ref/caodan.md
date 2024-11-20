# 使用 useRef 访问子组件

在 React 中，使用 `useRef` 访问子组件的 DOM 通常是通过 `forwardRef` 来实现的。

```jsx
import { useRef, forwardRef } from "react";

// 子组件的定义方式也要变化
// 使用forwardRef将ref传递给子组件
const ChildComponent = forwardRef((props, refFromParent) => {
  return (
    <div>
      {/* 把父组件的ref绑定到input上 */}
      <input ref={refFromParent} type="text" />
    </div>
  );
});

// 父组件
function App() {
  const childInputRef = useRef(null);

  const handleFocus = () => {
    // 操作的是子组件的input
    childInputRef.current.focus();
  };

  const handleGetValue = () => {
    // 操作的是子组件的input
    const value = childInputRef.current.value;
    console.log("Input value:", value);
  };

  return (
    <div>
      {/* 把ref传给子组件 */}
      <ChildComponent ref={childInputRef} />
      <button onClick={handleFocus}>Focus Input</button>
      <button onClick={handleGetValue}>Get Input Value</button>
    </div>
  );
}

export default App;
```
