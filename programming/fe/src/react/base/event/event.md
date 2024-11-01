# 事件绑定

语法 `on事件名={回调函数}`。

```jsx
function App() {
  const showMessage = () => {
    alert("hello");
  };

  return (
    <div>
      <button onClick={showMessage}>show</button>
    </div>
  );
}

export default App;
```
