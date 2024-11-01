# 函数形式的组件

1. 创建组件 Home.js:

```jsx
function Home() {
  return <div>Home</div>;
}

export default Home;
```

2. 在 App.js 中使用:

```jsx
import Home from "./Home";

function App() {
  return (
    <div>
      <Home />
    </div>
  );
}

export default App;
```
