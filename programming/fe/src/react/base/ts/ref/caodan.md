# 使用 useRef 访问子组件

```tsx
import { useRef, forwardRef } from "react";

interface PropsType {}

// 子组件
// forwardRef泛型的第一个参数是ref的类型, 第二个参数是组件的props类型
const ChildComponent = forwardRef<HTMLInputElement, PropsType>(
  (props, refFromParent) => {
    return (
      <div>
        <input ref={refFromParent} type="text" />
      </div>
    );
  }
);

// 父组件
function App() {
  const childInputRef = useRef<HTMLInputElement>(null);

  const handleFocus = () => {
    childInputRef.current?.focus();
  };

  const handleGetValue = () => {
    const value = childInputRef.current?.value;
    console.log("Input value:", value);
  };

  return (
    <div>
      <ChildComponent ref={childInputRef} />
      <button onClick={handleFocus}>Focus Input</button>
      <button onClick={handleGetValue}>Get Input Value</button>
    </div>
  );
}

export default App;
```

## 限制父组件访问的内容

```tsx
import { useRef, useImperativeHandle, forwardRef } from "react";

interface PropsType {}

interface RefType {
  focusInput: () => void;
  getInputValue: () => string;
}

// 子组件
const ChildComponent = forwardRef<RefType, PropsType>(
  (props, refFromParent) => {
    // ! 表示inputRef.current一定会有值
    // 使用的时候就不用?了
    const inputRef = useRef<HTMLInputElement>(null!);

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
  }
);

// 父组件
function App() {
  const childRef = useRef<RefType>(null);

  // 调用子组件的方法
  const handleFocus = () => {
    childRef.current?.focusInput();
  };

  // 调用子组件的方法
  const handleGetValue = () => {
    const value = childRef.current?.getInputValue();
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

export default App;
```
