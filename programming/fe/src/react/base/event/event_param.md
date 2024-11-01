# 获取 event 参数

```jsx
function App() {
  const showMessage = (message, e) => {
    console.log(message);
    console.log(e.target);
  };

  return (
    <div>
      <button
        onClick={(e) => {
          showMessage("hello", e);
        }}
      >
        show
      </button>
    </div>
  );
}

export default App;
```
