# 通过 props 通信

调用父组件传过来的函数, 并传递参数。

1. 父组件

```jsx
import Article from "./Article";

function App() {
  const callParentMethod = (params) => {
    console.log(params);
  };
  return (
    <div>
      <Article method1={callParentMethod} />
    </div>
  );
}

export default App;
```

2. 子组件

```jsx
function Article(props) {
  const { method1 } = props;
  return (
    <div>
      <button onClick={() => method1("Hello from Article")}>
        向父组件传值
      </button>
    </div>
  );
}

export default Article;
```
