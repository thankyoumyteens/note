# 传递参数

```jsx
function App() {
  const showMessage = (message) => {
    console.log(message);
  };

  return (
    <div>
      <button
        onClick={() => {
          showMessage("hello");
        }}
      >
        show
      </button>
    </div>
  );
}

export default App;
```
