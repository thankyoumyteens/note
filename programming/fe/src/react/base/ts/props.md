# 声明 props 类型

```tsx
// 声明props接收的类型
interface ChildProps {
  name?: string;
  age?: number;
}

function Child(props: ChildProps) {
  return (
    <div>
      <h1>name: {props.name}</h1>
      <h1>age: {props.age}</h1>
    </div>
  );
}
function App() {
  return (
    <div>
      <Child name="jack" age={18} />
    </div>
  );
}

export default App;
```

## 简写

```tsx
function Child({ name, age }: ChildProps) {
  return (
    <div>
      <h1>name: {name}</h1>
      <h1>age: {age}</h1>
    </div>
  );
}
```
