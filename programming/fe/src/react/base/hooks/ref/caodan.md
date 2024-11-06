# 使用 useRef 访问子组件

在 React 中，使用 `useRef` 访问子组件的方法通常是通过 `forwardRef` 和 `useImperativeHandle` 来实现的。

步骤：

1. 使用 `forwardRef`：将 `ref` 传递给子组件
2. 使用 `useImperativeHandle`：定义子组件中可以被外部访问的方法
3. 在父组件中使用 `useRef`：创建一个 `ref` 并将其传递给子组件

## 子组件

```jsx
import { useRef, useImperativeHandle, forwardRef } from "react";

// 使用forwardRef将ref传递给子组件
const ChildComponent = forwardRef((props, ref) => {
  // inputRef是一个普通的ref，用于访问输入框的DOM元素
  const inputRef = useRef(null);

  // 使用useImperativeHandle定义子组件中可以被外部访问的方法
  useImperativeHandle(ref, () => ({
    focusInput: () => {
      inputRef.current.focus();
    },
    getInputValue: () => {
      return inputRef.current.value;
    },
  }));

  return (
    <div>
      <input ref={inputRef} type="text" placeholder="Type something..." />
    </div>
  );
});

export default ChildComponent;
```

## 父组件

```jsx
import { useRef } from "react";
import ChildComponent from "./ChildComponent";

const ParentComponent = () => {
  // 使用useRef创建一个ref，并将其传递给子组件
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
};

export default ParentComponent;
```
