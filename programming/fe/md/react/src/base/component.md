# 使用组件

1. 创建 `src/components/UrlEncoder/UrlEncoder.tsx`:

```tsx
import React from "react";

class UrlEncoder extends React.Component {
  render() {
    return <div>UrlEncoder</div>;
  }
}

export default UrlEncoder;
```

2. 在 `src/App.tsx` 中使用:

```tsx
import React from "react";
import "./App.css";
import UrlEncoder from "./components/UrlEncoder/UrlEncoder";

const App: React.FC = () => (
  <div>
    <UrlEncoder />
  </div>
);

export default App;
```
