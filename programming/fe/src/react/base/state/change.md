# 修改 state

只有通过 setState 函数修改 state 中的数据, react 才会响应式地重绘页面。

```jsx
class MyApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "React",
    };
  }
  render() {
    return (
      <div>
        <span>Hello {this.state.name}</span>
        {/* 使用 setState 函数修改state中的数据 */}
        {/* 参数的对象中只需要传入要修改的数据即可 */}
        <button onClick={() => this.setState({ name: "World" })}>Change</button>
      </div>
    );
  }
}
```
