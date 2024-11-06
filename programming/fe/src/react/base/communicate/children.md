# children

父组件在子组件标签中写的内容, 会被传递到子组件 props 的 children 属性中。

1. 父组件

```jsx
import Article from "./Article";

function App() {
  const articleData = {
    title: "React",
    content: "A JavaScript library for building user interfaces",
  };
  return (
    <div>
      <Article>
        <h1>{articleData.title}</h1>
        <p>{articleData.content}</p>
      </Article>
    </div>
  );
}

export default App;
```

2. 子组件

```jsx
function Article(props) {
  const { children } = props;
  // 直接展示父组件传递的 h1 和 p 标签
  return <div>{children}</div>;
}

export default Article;
```

## 把标签传递到具体的 props 属性中

1. 父组件

```jsx
import Article from "./Article";

function App() {
  const articleData = {
    title: "React",
    author: "Facebook",
    content: "A JavaScript library for building user interfaces",
  };
  return (
    <div>
      <Article
        title={<h1>{articleData.title}</h1>}
        author={<h2>{articleData.author}</h2>}
      >
        {/* 不指定名称就会传到children中 */}
        <p>{articleData.content}</p>
      </Article>
    </div>
  );
}

export default App;
```

2. 子组件

```jsx
function Article(props) {
  const { title, author, children } = props;
  return (
    <div>
      {title}
      {author}
      {children}
    </div>
  );
}

export default Article;
```
