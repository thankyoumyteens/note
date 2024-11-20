# 使用 useRef 保存变量

错误写法:

```jsx
import { useState } from "react";

function App() {
  const [now, setNow] = useState(new Date().getTime());
  // 每次state变化都会重新执行App函数
  // timer也会被重新置位null
  let timer = null; // 错误

  const startIncrement = () => {
    // 开启定时器更新now的值
    timer = setInterval(() => {
      setNow(new Date().getTime());
    }, 1000);
  };
  const stopIncrement = () => {
    clearInterval(timer);
  };

  return (
    <div>
      <p>{now}</p>
      <button onClick={startIncrement}>开始</button>
      <button onClick={stopIncrement}>停止</button>
    </div>
  );
}

export default App;
```

## 使用 ref 解决

```tsx
import { useRef, useState } from "react";

function App() {
  const [now, setNow] = useState(new Date().getTime());
  // 每次重新执行App函数后,
  // ref的值不会丢失
  const timer = useRef(null);

  const startIncrement = () => {
    timer.current = setInterval(() => {
      setNow(new Date().getTime());
    }, 1000);
  };
  const stopIncrement = () => {
    clearInterval(timer.current);
  };

  return (
    <div>
      <p>{now}</p>
      <button onClick={startIncrement}>开始</button>
      <button onClick={stopIncrement}>停止</button>
    </div>
  );
}

export default App;
```
