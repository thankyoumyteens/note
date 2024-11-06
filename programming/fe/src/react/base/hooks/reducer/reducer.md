# useReducer

`useReducer` 提供了一种更加灵活的方式来管理组件的状态，特别是在状态逻辑复杂的情况下。通过将状态更新逻辑抽象成独立的 `reducer` 函数，可以使组件保持干净，逻辑更加清晰。

主要用途：

1. 复杂的状态逻辑：当组件的状态逻辑变得复杂，涉及到多个子状态之间的交互时，使用 `useReducer` 可以使代码更加模块化和易于理解
2. 全局状态管理

`useReducer` 接受三个参数：

- Reducer 函数：`(state, action) => newState`，它接收当前的状态和一个描述如何改变状态的动作（action），然后返回新的状态
- 初始状态：这是状态的初始值
- 初始化函数：这是一个可选参数，用于初始化状态，尤其是在状态初始化时需要执行一些昂贵的操作时非常有用

## 封装复杂的状态操作

```jsx
import { useReducer } from "react";

// 自定义reducer函数, 它接收当前的状态和一个描述如何改变状态的动作
function countReducer(state, action) {
  switch (action.type) {
    case "INCREMENT":
      // 返回新的state
      return { count: state.count + 1 };
    case "DECREMENT":
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function App() {
  // useReducer接收一个reducer函数和初始状态, 返回当前状态和dispatch函数
  // dispatch函数用于触发reducer函数, 从而更新状态
  const [state, dispatch] = useReducer(countReducer, { count: 0 });
  return (
    <div>
      <p>{state.count}</p>
      <button onClick={() => dispatch({ type: "INCREMENT" })}>+1</button>
      <button onClick={() => dispatch({ type: "DECREMENT" })}>-1</button>
    </div>
  );
}

export default App;
```
