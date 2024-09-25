# 使用组件

## 函数形式

1. 创建 `src/components/UrlEncoder/UrlEncoder.js`:

```jsx
import React from "react";

function UrlEncoder() {
  return <div>UrlEncoder</div>;
}

export default UrlEncoder;
```

2. 在 `src/App.js` 中使用:

```jsx
import UrlEncoder from "./components/UrlEncoder/UrlEncoder";

function App() {
  return (
    <div>
      <UrlEncoder />
    </div>
  );
}

export default App;
```

## 类形式

1. 创建 `src/components/UrlEncoder/UrlEncoder.js`:

```jsx
import React from "react";

class UrlEncoder extends React.Component {
  render() {
    return <div>UrlEncoder</div>;
  }
}

export default UrlEncoder;
```

2. 在 `src/App.js` 中使用:

```jsx
import UrlEncoder from "./components/UrlEncoder/UrlEncoder";

function App() {
  return (
    <div>
      <UrlEncoder />
    </div>
  );
}

export default App;
```
