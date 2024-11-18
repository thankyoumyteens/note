# 基本使用

### 1. 安装

```sh
npm install react-router-dom
```

### 2. 定义路由 router/index.tsx

```tsx
import { createBrowserRouter } from "react-router-dom";
// 引入路由用到的组件
import Home from "../components/Home";
import About from "../components/About.tsx";

// 定义路由
const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/about",
    element: <About />,
  },
]);

export default router;
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
