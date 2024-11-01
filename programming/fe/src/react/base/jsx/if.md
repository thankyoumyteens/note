# 条件渲染

使用 `&&` 或三元表达式实现条件渲染。

```jsx
function App() {
  let showMessage = true;
  return (
    <div>
      {showMessage && <h1>hello</h1>}
      {showMessage ? <h1>hello</h1> : null}
    </div>
  );
}

export default App;
```

## 复杂条件

```jsx
function getMessage(status) {
  switch (status) {
    case "01":
      return <h1>hello</h1>;
    case "02":
      return <h1>hi</h1>;
    default:
      return null;
  }
}

function App() {
  let status = "01";

  return <div>{getMessage(status)}</div>;
}

export default App;
```
