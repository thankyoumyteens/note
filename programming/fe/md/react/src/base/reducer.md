# reducer

reducer 是一个函数，它负责管理状态（state）的更新。这个函数接收两个参数：当前状态（current state）和动作（action），然后返回新的状态。useReducer 钩子是 React 提供的一种状态管理方式，它适用于管理复杂的状态逻辑。与 useState 钩子相比，useReducer 更适合处理多个子值的状态更新。

`reducer`的执行流程：

1. **初始化状态**：当组件首次渲染时，`useReducer`钩子会调用`reducer`函数一次，传入初始状态和`undefined`作为动作（action）。这允许你为组件设置初始状态。

2. **分发动作**：当组件需要更新状态时，会调用`dispatch`函数，并传递一个描述状态如何变化的动作对象。动作对象通常包含一个`type`属性，以及可能的额外数据。

3. **调用`reducer`**：`dispatch`函数的调用会导致`reducer`函数再次被调用。这次，它接收当前的状态和刚刚分发的动作作为参数。

4. **计算新状态**：`reducer`函数根据传入的动作类型和当前状态来决定如何更新状态。它通过`switch`语句或`if`逻辑来处理不同的动作类型，并返回新的状态对象。

5. **返回新状态**：`reducer`函数返回新的状态对象后，React 将使用这个新状态来更新组件。如果新状态与旧状态相同，组件将跳过重新渲染。

6. **组件重新渲染**：状态更新后，组件会根据新状态重新渲染。如果`reducer`函数返回的状态与当前状态相同（即没有变化），组件将不会重新渲染，这是一种性能优化。

7. **循环**：组件的渲染和状态更新是一个循环过程。每当`dispatch`被调用，上述流程就会重复执行。

```jsx
import React from "react";

function App() {
  // 在reducer函数中处理action
  const myReducer = (oldListData, action) => {
    switch (action.type) {
      case "add":
        let newListData = [...oldListData];
        newListData.push(action.value);
        return newListData;
      default:
        return oldListData;
    }
  };
  // 定义reducer, 设置reducer函数, 并把myList初始化为 []
  const [myList, dispatch] = React.useReducer(myReducer, []);

  return (
    <div>
      <div>
        {/* 列表 */}
        <ul>
          {myList.map((item, index) => (
            <li key={index}>{item.name}</li>
          ))}
        </ul>
      </div>
      <button
        onClick={() => {
          /* 设置action */
          const action = {
            type: "add",
            value: {
              id: myList.length + 1,
              name: `Name ${myList.length + 1}`,
            },
          };
          /* 触发action */
          dispatch(action);
        }}
      >
        添加列表项
      </button>
    </div>
  );
}

export default App;
```
