# JSX

JSX 允许 HTML 与 JavaScript 混写

遇到 HTML 标签(以 `<` 开头), 就用 HTML 规则解析。遇到代码块(以 `{` 开头), 就用 JavaScript 规则解析。

```jsx
import React from "react";

const isShow = true;
const helloworld = "Hello World";

function App() {
  return (
    // 以 < 开头, 用 HTML 规则解析
    <div>
      {/* 以 { 开头, 用 JavaScript 规则解析 */}
      {isShow ? helloworld : "none"}
    </div>
  );
}

export default App;
```

## 样式类名

样式的类名不要用`class`, 要用`className`

```jsx
import React from "react";
import "./App.css";

function App() {
  return <div className="hello-main"></div>;
}

export default App;
```

## 内联样式

内联样式, 要用`style={{key:value}}`的形式, 并且 key 要使用驼峰

```jsx
import React from "react";

function App() {
  return (
    <div
      style={{
        width: 100,
        height: 100,
        backgroundColor: "blue",
      }}
    ></div>
  );
}

export default App;
```

也可以写成

```jsx
import React from "react";

const myStyle = {
  width: 100,
  height: 100,
  backgroundColor: "blue",
};

function App() {
  return <div style={myStyle}></div>;
}

export default App;
```

## 标签名

若标签首字母以小写字母开头, react 就会把它作为 html 标签渲染, 若 html 中无该标签, 则报错。若标签首字母以大写字母开头, react 就会把它作为组件渲染, 若组件没有定义, 则报错。

```jsx
import React from "react";

class HelloWorld extends React.Component {
  render() {
    return <h1>Hello World</h1>;
  }
}

function App() {
  return (
    <div>
      <HelloWorld />
    </div>
  );
}

export default App;
```

## 给属性赋值

使用大括号可以直接给 html 标签的属性赋值

```jsx
import React from "react";

const imgPath = require("./images/1.jpg");

function App() {
  return (
    <div>
      <img src={imgPath.default} alt="1" />
    </div>
  );
}

export default App;
```

## 渲染列表

```jsx
import React from "react";

const listData = [
  {
    id: 1,
    name: "John",
    age: 25,
  },
  {
    id: 2,
    name: "Doe",
    age: 30,
  },
  {
    id: 3,
    name: "Jane",
    age: 22,
  },
];

function App() {
  return (
    <div>
      <ul>
        {listData.map((data) => (
          <li key={data.id}>
            {data.name} - {data.age}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

## 事件处理

```jsx
import React from "react";

function App() {
  return (
    <div
      onClick={() => {
        alert("点击了");
      }}
    >
      点击
    </div>
  );
}

export default App;
```
