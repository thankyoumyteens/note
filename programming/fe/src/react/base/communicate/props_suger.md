# 解构语法

可以通过解构语法简化 props 的传递。

```jsx
import Article from "./Article";

function App() {
  const articleData = {
    title: "React",
    content: "A JavaScript library for building user interfaces",
  };
  return (
    <div>
      <Article title={articleData.title} content={articleData.content} />
      {/* 和上面的方式是等价的 */}
      <Article {...articleData} />
    </div>
  );
}

export default App;
```
