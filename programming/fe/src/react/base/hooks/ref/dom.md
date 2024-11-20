# 使用 useRef 访问 DOM

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
