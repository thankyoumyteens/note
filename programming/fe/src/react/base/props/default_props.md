# props 默认值

```jsx
class Person extends React.Component {
  // 设置默认值
  static defaultProps = {
    title: "Person Info",
    personInfo: {
      name: "Unknown",
      age: 0,
    },
  };
  render() {
    const { title, personInfo } = this.props;
    const { name, age } = personInfo;
    return (
      <div>
        <h1>{title}</h1>
        <p>
          {name} is {age} years old
        </p>
      </div>
    );
  }
}
```
