# 通过 props 通信

父传子: 通过 props 传递。

子传父: 调用父组件传过来的函数, 并传递参数。

1. 父组件

```jsx
import { useState } from "react";
import Home from "./Home";

function App() {
  const [data, setData] = useState({
    title: "标题",
    content: "内容",
  });
  return (
    <div>
      <Home data={data} setData={setData} />
    </div>
  );
}

export default App;
```

2. 子组件

```jsx
function Home(props) {
  const { data, setData } = props;
  const changeData = () => {
    setData({
      ...data,
      content: "新内容",
    });
  };
  return (
    <div>
      <h1>{data.title}</h1>
      <p>{data.content}</p>
      <button onClick={changeData}>切换内容</button>
    </div>
  );
}

export default Home;
```
