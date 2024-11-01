# js 表达式

标签中混入 JS 表达式时要用 `{}` 包起来。注意只能使用表达式, 不能使用 if、switch、for 等语句。

```jsx
function App() {
  const name = "Tom";
  return <div>Hello, {name}</div>;
}

export default App;
```
