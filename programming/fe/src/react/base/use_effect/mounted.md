# 组件渲染完毕后调用

```jsx
import { useEffect } from "react";

function App() {
  // 组件渲染完毕后调用
  useEffect(() => {
    console.log("组件渲染完毕");
  }, []);
  return <div></div>;
}

export default App;
```
