# props 传递 jsx 标签

```tsx
interface ChildProps {
  info: JSX.Element; // 表示这是一个 JSX 标签
}

function Child({ info }: ChildProps) {
  return <div>{info}</div>;
}
function App() {
  const info = <div>hello world</div>;
  return (
    <div>
      <Child info={info} />
    </div>
  );
}

export default App;
```
