# 基本用法

```jsx
class Person extends React.Component {
  render() {
    // 通过props使用父组件传来的数据
    const { name, age } = this.props.personInfo;
    return (
      <div>
        {name} is {age} years old
      </div>
    );
  }
}

class MyApp extends React.Component {
  state = {
    person: {
      name: "John",
      age: 10,
    },
  };
  render() {
    return (
      <div>
        {/* 向子组件传递数据 */}
        <Person personInfo={this.state.person} />
      </div>
    );
  }
}
```
