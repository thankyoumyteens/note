# Context

使用 createContext 创建上下文对象, 上层组件通过 Provider 组件提供数据, 底层组件通过 useContext 获取数据。

1. 定义 Context

```js
import { createContext } from "react";
const TitleContext = createContext();
export default TitleContext;
```

2. 上级组件提供数据

```jsx
import Home from "./Home";
import TitleContext from "./TitleContext";

function App() {
  const title = "标题";

  return (
    <div>
      <TitleContext.Provider value={title}>
        <Home />
      </TitleContext.Provider>
    </div>
  );
}

export default App;
```

3. 下(多)级组件使用数据

```jsx
import { useContext } from "react";
import TitleContext from "./TitleContext";

function Title() {
  const title = useContext(TitleContext);
  return <div>{title}</div>;
}

export default Title;
```
