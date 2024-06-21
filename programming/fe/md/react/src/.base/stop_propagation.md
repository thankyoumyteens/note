# 阻止事件冒泡

```jsx
function App() {
  const outerClick = () => {
    alert("outer click");
  };

  const divClick = (event) => {
    // 阻止事件冒泡
    event.stopPropagation();
    alert("div click");
  };

  return (
    <div onClick={outerClick}>
      <div onClick={divClick}>div</div>
    </div>
  );
}

export default App;
```
