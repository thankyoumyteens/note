# 父子组件通信

## 函数形式

```jsx
import React from "react";

function Child({ parentCount, parentChangeCount }) {
  return (
    <div>
      {/* 子组件调用父组件的函数向父组件传值 */}
      <button onClick={() => parentChangeCount(parentCount + 1)}>
        Increment
      </button>
    </div>
  );
}
// 也可以写成:
// function Child(props) {
//   return (
//     <div>
//       <button onClick={() => props.parentChangeCount(props.parentCount + 1)}>
//         Increment
//       </button>
//     </div>
//   );
// }

function Parent() {
  const [count, setCount] = React.useState(0);

  const changeCount = (newCount) => {
    setCount(newCount);
  };

  return (
    <div>
      <p>Count: {count}</p>
      {/* 父组件传递 变量count和函数changeCount 给子组件 */}
      {/* parentCount是count在子组件中的名称 */}
      {/* parentChangeCount是changeCount在子组件中的名称 */}
      {/* count的值变化后, parentCount会同步变化 */}
      <Child parentCount={count} parentChangeCount={changeCount} />
    </div>
  );
}

function App() {
  return (
    <div>
      <Parent />
    </div>
  );
}

export default App;
```

## 子组件向父组件传递数据
