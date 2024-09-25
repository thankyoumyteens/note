# 多层组件通信

组件层级:

```
App
├── Header
└── Body
    └── Content
```

要实现在 Content 中访问 App 的 state。

1. 创建 context

```js
// MyContext.js
import React from "react";

const myContext = React.createContext({});

export default myContext;
```

2. Header

```js
// Header.js
function Header({ changeMyVal }) {
  return (
    <header>
      <h1>My Website</h1>
      {/* 改变state的值 */}
      <button onClick={() => changeMyVal({ name: "changed" })}>
        change name
      </button>
    </header>
  );
}

export default Header;
```

3. 在 App 中为 context 赋值

```js
// App.js
import React from "react";
import Header from "./Header";
import Body from "./Body";
import myContext from "./MyContext";

function App() {
  const [myVal, setMyVal] = React.useState({
    name: "Winnie",
  });
  return (
    <div>
      {/* 把context初始化为myVal */}
      <myContext.Provider value={myVal}>
        {/* myContext标签下的所有组件都能获取到这个context */}
        <Header changeMyVal={setMyVal} />
        <Body />
      </myContext.Provider>
    </div>
  );
}

export default App;
```

4. 在 Content 中获取 context

```js
// Content.js
import React from "react";
import myContext from "./MyContext";

function Content() {
  // 获取context
  const myVal = React.useContext(myContext);

  return (
    <div>
      <h1>Content</h1>
      {/* 使用context中的state */}
      <p>{myVal.name}</p>
    </div>
  );
}

export default Content;
```
