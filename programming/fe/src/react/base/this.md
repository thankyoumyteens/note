# this 指向问题

```jsx
class MyApp extends React.Component {
  constructor(props) {
    // constructor中的this指向MyApp组件的实例
    super(props);
    this.state = {
      name: "React",
    };
  }
  render() {
    // render中的this指向MyApp组件的实例
    return (
      <div>
        <span>Hello {this.state.name}</span>

        {/* 点击时报错: Cannot read properties of undefined (reading 'setState') */}
        {/* 因为changeValue方法是作为onClick的回调函数被调用的 */}
        {/* 调用changeValue方法的对象不是MyApp组件的实例 */}
        {/* 所以changeValue中的this也不是MyApp组件的实例 */}
        <button onClick={this.changeValue}>Change1</button>
        {/* 可以使用 */}
        {/* 手动把MyApp组件的实例绑定到changeValue方法的this */}
        <button onClick={this.changeValue.bind(this)}>Change2</button>
        {/* 可以使用 */}
        {/* 箭头函数的this固定是它定义时上下文的this */}
        {/* 而不会随着调用方的不同而改变 */}
        <button
          onClick={() => {
            // this是MyApp组件的实例
            // 这里是用MyApp组件的实例调用changeValue方法
            this.changeValue();
          }}
        >
          Change3
        </button>
      </div>
    );
  }
  changeValue() {
    // changeValue中的this指向取决于调用这个方法的对象
    // 不一定是MyApp组件的实例
    this.setState({ name: "World" });
  }
}
```
