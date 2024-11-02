# 获取 DOM

```jsx
import { useRef } from "react";

function App() {
  // 创建一个ref对象, 用于绑定到标签上
  const pElement = useRef(null);
  const changeColor = () => {
    console.log(pElement);
    pElement.current.style.color = "red";
  };
  return (
    <div>
      <p ref={pElement}>aaa</p>
      <button onClick={changeColor}>变色</button>
    </div>
  );
}

export default App;
```
