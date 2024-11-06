# Context

使用 createContext 创建上下文对象, 上层组件通过 Provider 组件提供数据, 底层组件通过 useContext 获取数据。

1. 定义 Context

```js
// TitleContext.js
import { createContext } from "react";
const TitleContext = createContext();
export default TitleContext;
```

2. 在 App 组件中提供变量 title

```jsx
import TitleContext from "./TitleContext";
import Article from "./Article";

function App() {
  const title = "标题";
  return (
    <div>
      {/* 使用TitleContext.Provider包裹Article组件, 并传入title属性 */}
      {/* 这样Article组件及其所有下级组件就都可以通过TitleContext获取到title */}
      <TitleContext.Provider value={title}>
        <Article />
      </TitleContext.Provider>
    </div>
  );
}

export default App;
```

3. Article 组件

```jsx
import Title from "./Title";

function Article(props) {
  return (
    <div>
      <Title />
    </div>
  );
}

export default Article;
```

4. 在 Title 组件中使用 title

```jsx
import { useContext } from "react";
import TitleContext from "./TitleContext";

function Title() {
  // 通过useContext获取TitleContext中的title
  const title = useContext(TitleContext);
  return <div>{title}</div>;
}

export default Title;
```
