# memo

问题: 虽然 Child 子组件没用到 age, 但是 age 的变化也会导致 Child 组件重新渲染。

```jsx
import { useState } from "react";

function Child({ name }) {
  console.log("子组件重新渲染了");
  return <div>Child: {name}</div>;
}

function App() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  return (
    <div>
      姓名: <input value={name} onChange={(e) => setName(e.target.value)} />
      年龄: <input value={age} onChange={(e) => setAge(e.target.value)} />
      <Child name={name} />
    </div>
  );
}

export default App;
```

## 使用 memo

memo 会缓存子组件, 只有子组件用到的状态变化时, 才会重新渲染子组件。此时 age 的变化不会导致 Child 组件重新渲染。

```jsx
import { memo, useState } from "react";

const Child = memo(({ name }) => {
  console.log("子组件重新渲染了");
  return <div>Child: {name}</div>;
});

function App() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  return (
    <div>
      姓名: <input value={name} onChange={(e) => setName(e.target.value)} />
      年龄: <input value={age} onChange={(e) => setAge(e.target.value)} />
      <Child name={name} />
    </div>
  );
}

export default App;
```

## 手动指定缓存规则

```jsx
import { memo, useState } from "react";

const Child = memo(
  ({ name }) => {
    console.log("子组件重新渲染了");
    return <div>Child: {name}</div>;
  },
  (oldProps, newProps) => {
    //  返回 true 表示使用缓存, 返回 false 表示不使用缓存
    if (oldProps.name === newProps.name) {
      // 如果 name 没有变化, 直接使用缓存, 不重新渲染
      return true;
    }
    // 使用最新的值, 重新渲染
    return false;
  }
);

function App() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  return (
    <div>
      姓名: <input value={name} onChange={(e) => setName(e.target.value)} />
      年龄: <input value={age} onChange={(e) => setAge(e.target.value)} />
      <Child name={name} />
    </div>
  );
}

export default App;
```
