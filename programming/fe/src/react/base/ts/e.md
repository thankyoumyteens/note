# 事件参数类型

```tsx
function App() {
  const handleClick = (e: React.MouseEvent) => {
    console.log(e);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };

  return (
    <div>
      <button onClick={handleClick}>点击</button>
      <input type="text" onChange={handleChange} />
    </div>
  );
}

export default App;
```
