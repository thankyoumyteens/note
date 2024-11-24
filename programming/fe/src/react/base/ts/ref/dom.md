# 使用 useRef 访问 DOM

```tsx
import { useRef } from "react";

function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const focusInput = () => inputRef.current?.focus();
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
