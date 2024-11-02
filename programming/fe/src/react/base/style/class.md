# css 类

1. 定义样式

```css
.div-style {
  font-size: 20px;
}
```

2. 使用样式

```jsx
import { useState } from "react";
import "./index.css";

function App() {
  const [needStyle, setNeedStyle] = useState(true);
  return (
    <div>
      <div className={`common-style ${needStyle && "div-style"}`}>ok</div>
    </div>
  );
}

export default App;
```
