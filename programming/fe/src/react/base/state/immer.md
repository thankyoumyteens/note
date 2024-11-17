# useImmer

useImmer 用来简化 state 中修改对象和数组的写法。

### 1. 安装

```sh
npm install use-immer
```

### 2. 修改对象

```jsx
import { useImmer } from "use-immer";

function App() {
  const [data, setData] = useImmer({
    value: 1,
  });

  const changeValue = () => {
    // 修改对象的值
    setData((draft) => {
      draft.value += 1;
    });
  };
  return (
    <div>
      <h1>{data.value}</h1>
      <button onClick={changeValue}>Change Value</button>
    </div>
  );
}

export default App;
```

### 3. 修改数组

```jsx
import { useImmer } from "use-immer";

function App() {
  const [data, setData] = useImmer([0, 1, 2]);

  const changeValue = () => {
    // 修改数组的值
    setData((draft) => {
      draft[1] += 1;
    });
  };
  return (
    <div>
      <h1>{data[1]}</h1>
      <button onClick={changeValue}>Change Value</button>
    </div>
  );
}

export default App;
```
