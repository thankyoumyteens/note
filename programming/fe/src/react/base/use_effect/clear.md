# 组件卸载时调用

```jsx
import { useEffect } from "react";

function App() {
  useEffect(() => {
    console.log("组件渲染完毕");
    // 组件卸载时调用
    return () => {
      console.log("组件卸载");
    };
  }, []);
  return <div></div>;
}

export default App;
```
