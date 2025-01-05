# 使用 useRef 访问子组件

在 React 中, 使用 `useRef` 访问子组件的 DOM 通常是通过 `forwardRef` 来实现的。

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

## 限制父组件访问的内容

```jsx
import { useRef, useImperativeHandle, forwardRef } from "react";

// 子组件

// 使用forwardRef将ref传递给子组件
const ChildComponent = forwardRef((props, refFromParent) => {
  // inputRef是一个普通的ref, 用于访问输入框的DOM元素
  const inputRef = useRef(null);

  // 使用useImperativeHandle定义子组件中可以被外部访问的方法
  useImperativeHandle(refFromParent, () => ({
    focusInput: () => {
      inputRef.current.focus();
    },
    getInputValue: () => {
      return inputRef.current.value;
    },
  }));

  return (
    <div>
      <input ref={inputRef} type="text" />
    </div>
  );
});

// 父组件
function App() {
  // 使用useRef创建一个ref, 并将其传递给子组件
  const childRef = useRef(null);

  // 调用子组件的方法
  const handleFocus = () => {
    childRef.current.focusInput();
  };

  // 调用子组件的方法
  const handleGetValue = () => {
    const value = childRef.current.getInputValue();
    console.log("Input value:", value);
  };

  return (
    <div>
      <ChildComponent ref={childRef} />
      <button onClick={handleFocus}>Focus Input</button>
      <button onClick={handleGetValue}>Get Input Value</button>
    </div>
  );
}
```
