# State 

state 与 props 类似, 但是 state 是私有的, 并且完全受控于当前组件。

在相同的 DOM 节点中渲染 某个组件 , 就仅有一个该组件的 class 实例被创建使用。

# 初始化state

只能在构造函数中初始化state

```jsx
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date}.</h2>
      </div>
    );
  }
}
```

# 更新state

- 要使用 `this.setState()` 来更新组件的 state, 直接修改 state 时不会重新渲染组件
- 调用了`setState()`方法以后, 就会调用`render()`方法, 也就是前面说的, 用户的界面会随着状态的改变而改变。
- 当调用`setState()`, React会合并你提供的对象到当前的 state 里

```jsx
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        name: 'World',
        date: new Date()
    };
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }

  tick() {
    this.setState({
      date: new Date()
    });
  }

  render() {
    return (
      <div>
        <h1>Hello, {this.state.name}!</h1>
        <h2>It is {this.state.date}.</h2>
      </div>
    );
  }
}
```
