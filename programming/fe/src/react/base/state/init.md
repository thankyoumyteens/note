# 初始化 state

```jsx
class MyApp extends React.Component {
  constructor(props) {
    super(props);
    // 初始化state
    this.state = {
      name: "React",
    };
  }
  render() {
    // 使用stete中的数据
    return <div>Hello {this.state.name}</div>;
  }
}
```
