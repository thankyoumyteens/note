# 通过 props 通信

通过 props 传递。

1. 父组件

```jsx
import Article from "./Article";

function App() {
  const title = "Title 1";
  const content = "Content 1";
  return (
    <div>
      {/* 通过props向子组件传值 */}
      <Article title={title} content={content} />
    </div>
  );
}

export default App;
```

2. 子组件

```jsx
function Article(props) {
  // 通过props接收父组件传递过来的值
  const { title, content } = props;
  return (
    <div>
      <h1>{title}</h1>
      <p>{content}</p>
    </div>
  );
}

export default Article;
```
