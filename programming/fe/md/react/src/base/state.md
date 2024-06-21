# state

## 更新数据后, 自动更新页面

```jsx
import React from "react";

function App() {
  // count 初始化为0
  const [count, setCount] = React.useState(0);

  return (
    <div>
      <p>{count}</p>
      {/* 执行setCount后,会重新执行App函数来更新页面 */}
      <button onClick={() => setCount(count + 1)}>加一</button>
    </div>
  );
}

export default App;
```

## 更新对象/数组数据后, 自动更新页面

对象/数组的某些元素修改后不会触发页面的更新。需要在 setState 函数中传入一个新的对象/数组。

```jsx
import React from "react";

function App() {
  // count.val 初始化为0
  const [count, setCount] = React.useState({
    val: 0,
  });

  const changeCount = () => {
    // setCount 传入一个新的对象, 替换原来的对象
    setCount({ val: count.val + 1 });
  };

  return (
    <div>
      <p>{count.val}</p>
      {/* 执行setCount后,会重新执行App函数来更新页面 */}
      <button onClick={() => changeCount(count.val + 1)}>加一</button>
    </div>
  );
}

export default App;
```

数组同理:

```jsx
import React from "react";

function App() {
  // count.val 初始化为0
  const [count, setCount] = React.useState([0]);

  const changeCount = () => {
    // setCount 传入一个新的数组, 替换原来的数组
    setCount([count[0] + 1]);
  };

  return (
    <div>
      <p>{count[0]}</p>
      {/* 执行setCount后,会重新执行App函数来更新页面 */}
      <button onClick={() => changeCount(count[0] + 1)}>加一</button>
    </div>
  );
}

export default App;
```

## 多次更新的问题

多次调用 setCount 时, count 的值不会累加:

```jsx
import React from "react";

function App() {
  // count 初始化为0
  const [count, setCount] = React.useState(0);

  const changeCount = () => {
    // 这么写,只会加一
    setCount(count + 1);
    setCount(count + 1);
  };

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => changeCount()}>加二</button>
    </div>
  );
}

export default App;
```

正确写法:

```jsx
import React from "react";

function App() {
  // count 初始化为0
  const [count, setCount] = React.useState(0);

  const changeCount = () => {
    // 写成函数的形式, 后面的函数可以获取到前一个函数修改的最新的count值
    setCount((count) => count + 1);
    setCount((count) => count + 1);
  };

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => changeCount()}>加二</button>
    </div>
  );
}

export default App;
```
