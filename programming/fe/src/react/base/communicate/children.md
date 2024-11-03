# children

父组件在子组件标签中写的内容, 会被传递到子组件 props 的 children 属性中。

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
      <Home>
        <h1>{data.title}</h1>
        <p>{data.content}</p>
      </Home>
    </div>
  );
}

export default App;
```

2. 子组件

```jsx
function Home(props) {
  const { children } = props;

  return <div>{children}</div>;
}

export default Home;
```
