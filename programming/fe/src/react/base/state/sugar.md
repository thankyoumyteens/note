# state 简写形式

```jsx
class MyApp extends React.Component {
  // 直接在类中定义
  state = {
    name: "React",
  };
  // 使用箭头函数处理this指向
  changeValue = () => {
    this.setState({ name: "World" });
  };
  render() {
    return (
      <div>
        <span>Hello {this.state.name}</span>
        <button onClick={this.changeValue}>Change</button>
      </div>
    );
  }
}
```
