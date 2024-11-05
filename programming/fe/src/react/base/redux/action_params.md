# action 传参

1. 修改 store/modules/counterStore.js

```js
import { createSlice } from "@reduxjs/toolkit";

const counterStore = createSlice({
  name: "counter",
  initialState: {
    count: 0,
  },
  reducers: {
    add(state, action) {
      // action.payload是调用时传入的参数
      state.count += action.payload;
    },
    sub(state, action) {
      state.count -= action.payload;
    },
  },
});

// 导出actions
export const { add, sub } = counterStore.actions;
export default counterStore.reducer;
```

2. 在组件中使用

```jsx
import { useDispatch, useSelector } from "react-redux";
import { add, sub } from "./store/modules/counterStore";

function App() {
  const { count } = useSelector((state) => state.counter);
  const dispatch = useDispatch();
  return (
    <div>
      <h1>{count}</h1>
      {/* 调用action时传参 */}
      <button onClick={() => dispatch(add(100))}>+</button>
      <button onClick={() => dispatch(sub(100))}>-</button>
    </div>
  );
}

export default App;
```
