# 基本使用

1. 创建 store/modules/counterStore.js

```js
import { createSlice } from "@reduxjs/toolkit";

// 创建一个slice
const counterStore = createSlice({
  name: "counter",
  // 初始化state
  initialState: {
    count: 0,
  },
  // 定义两个用来修改state的方法
  reducers: {
    increment(state) {
      state.count += 1;
    },
    decrement(state) {
      state.count -= 1;
    },
  },
});

// 导出actions
export const { increment, decrement } = counterStore.actions;
// 导出reducer
export default counterStore.reducer;
```

2. 创建 store/index.js

```js
import { configureStore } from "@reduxjs/toolkit";
import counter from "./modules/counterStore";

// 通过configureStore方法创建store
export default configureStore({
  reducer: {
    counter: counter,
  },
});
```

3. 修改 index.js 注入 store

```js
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import store from "./store";
import { Provider } from "react-redux";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
```

4. 在组件中使用

```jsx
import { useDispatch, useSelector } from "react-redux";
import { increment, decrement } from "./store/modules/counterStore";

function App() {
  // 获取counterStore中的count
  const { count } = useSelector((state) => state.counter);
  // 需要通过dispatch调用increment和decrement方法
  const dispatch = useDispatch();
  return (
    <div>
      <h1>{count}</h1>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  );
}

export default App;
```
