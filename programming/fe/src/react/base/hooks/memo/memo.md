# useMemo

`useMemo` 可以缓存某个值的计算结果，只有在依赖项发生变化时才会重新计算。类似于 vue 的 computed。

主要用途：

1. 性能优化：避免在每次渲染时执行昂贵的计算，特别是当这些计算结果不经常变化时
2. 减少不必要的重新渲染：确保依赖项发生变化时才重新计算，从而减少不必要的重新渲染

基本语法：

```javascript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

- `computeExpensiveValue(a, b)`：这是一个计算昂贵值的函数
- `[a, b]`：这是一个依赖数组，包含所有影响计算结果的变量。如果这些变量发生变化，`useMemo` 会重新计算并返回新的值

## 基本用法

假设你有一个组件需要根据两个数值计算一个昂贵的结果：

```jsx
import React, { useState, useMemo } from "react";

function ExpensiveComputation({ a, b }) {
  console.log("Expensive computation running");

  // 使用useMemo来缓存计算结果
  // 只有当a或b发生变化时, useMemo才会重新计算expensiveResult
  const expensiveResult = useMemo(() => {
    // 模拟一个耗时的计算
    let result = 0;
    for (let i = 0; i < 100000000; i++) {
      result += a * b;
    }
    return result;
  }, [a, b]); // 只有当 a 或 b 发生变化时重新计算

  return (
    <div>
      <p>Expensive Result: {expensiveResult}</p>
    </div>
  );
}

function App() {
  const [a, setA] = useState(1);
  const [b, setB] = useState(2);
  const [c, setC] = useState(0);

  return (
    <div>
      <ExpensiveComputation a={a} b={b} />
      <button onClick={() => setA(a + 1)}>Increment a</button>
      <button onClick={() => setB(b + 1)}>Increment b</button>
      {/* 即使c发生变化expensiveResult也不会重新计算，因为c不在依赖数组中 */}
      <button onClick={() => setC(c + 1)}>Increment c (no effect)</button>
    </div>
  );
}

export default App;
```
