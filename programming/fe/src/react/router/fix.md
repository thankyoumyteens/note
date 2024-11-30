# 固定页面部分元素

使用嵌套路由。

### 1.定义路由 router/index.tsx

```tsx
import { createBrowserRouter } from "react-router-dom";
import Home from "./Home";
import About from "./About";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    // 定义嵌套路由
    children: [
      // 注意前面没有/
      { path: "", element: <Home /> },
      { path: "about", element: <About /> },
    ],
  },
]);

export default router;
```

### 2. App.tsx

```tsx
import { Outlet } from "react-router-dom";
import Menu from "./components/Menu";

function App() {
  return (
    <div>
      {/* 展示菜单按钮 */}
      <Menu />
      {/* 展示嵌套路由的内容 */}
      <Outlet />
    </div>
  );
}

export default App;
```

### 3. 在 main.tsx 中引入

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import router from "./router";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
```
