# 动态配置路由

```tsx
import { createBrowserRouter, RouteObject } from "react-router-dom";
import { lazy } from "react";
import { getMenuList } from "../api/menu.ts";
import { Menu } from "../types";
import Login from "../components/Login.tsx";
import App from "../App.tsx";

// 定义基本路由
let routes: RouteObject[] = [
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/login",
    element: <Login />,
  },
];

// 调用后端接口获取数据
const res = await getMenuList();
const menuList = res.data;
// 遍历菜单列表，动态生成路由
menuList.forEach((menu: Menu) => {
  routes.push({
    path: menu.path,
    Component: lazy(() => import(`../components/${menu.component}`)),
  });
});
// 定义路由
const router = createBrowserRouter(routes);

export default router;
```
