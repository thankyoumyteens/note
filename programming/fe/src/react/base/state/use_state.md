# useState

useState 是 React Hook 函数, 可以向函数组件中添加一个状态变量(state)。

```jsx
import { useState } from "react";

function App() {
  // 定义状态变量count和修改count的函数setCount
  // useState(0)表示count的初始值为0
  const [count, setCount] = useState(0);

  const increment = () => {
    // count的值修改后，组件会重新渲染
    // 直接修改count的值组件不会重新渲染，需要通过setCount函数来修改
    setCount(count + 1);
  };
  return (
    <div>
      <div>{count}</div>
      <button onClick={increment}>增加</button>
    </div>
  );
}

export default App;
```
