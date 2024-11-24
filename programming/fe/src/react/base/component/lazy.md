# 组件懒加载

### 1. Home

```jsx
export default function Home() {
  return <div>Home</div>;
}
```

### 2. App

```jsx
import { lazy, Suspense } from "react";

// 组件懒加载
const Home = lazy(() => {
  return import("./Home");
});

function App() {
  return (
    <div>
      {/* fallback 指定组件加载完成之前/失败时显示的内容 */}
      <Suspense fallback={<div>加载中...</div>}>
        <Home />
      </Suspense>
    </div>
  );
}

export default App;
```
