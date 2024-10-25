# 类形式的组件

1. 创建组件 Home.js:

```jsx
import React from "react";

class Home extends React.Component {
  render() {
    return <div>Home</div>;
  }
}

export default Home;
```

2. 在 App.js 中使用:

```jsx
import Home from "./components/Home";

function App() {
  return (
    <div>
      <Home />
    </div>
  );
}

export default App;
```
