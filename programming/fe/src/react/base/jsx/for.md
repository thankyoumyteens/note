# 渲染列表

不能使用 for 语句, 要使用 js 的 map 方法渲染列表。

```jsx
function App() {
  let dataList = [
    { id: 1, name: "John" },
    { id: 2, name: "Doe" },
    { id: 3, name: "Jane" },
  ];
  // 使用js的map方法遍历dataList数组
  return (
    <div>
      <ul>
        {dataList.map((data) => (
          <li key={data.id}>{data.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

## 返回多个标签

可以用 Fragment 包起来, 相当于 template 标签。

```jsx
import { Fragment } from "react";

function App() {
  let dataList = [
    { id: 1, name: "John" },
    { id: 2, name: "Doe" },
    { id: 3, name: "Jane" },
  ];
  return (
    <div>
      <ul>
        {dataList.map((data) => (
          <Fragment key={data.id}>
            <li>{data.id}</li>
            <li>{data.name}</li>
          </Fragment>
        ))}
      </ul>
    </div>
  );
}

export default App;
```
