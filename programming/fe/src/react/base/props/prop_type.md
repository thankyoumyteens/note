# 限制 props 类型

1. 安装

```sh
npm install --save prop-types
```

2. 使用

```jsx
import PropTypes from "prop-types";

class Person extends React.Component {
  // 限制传入的 props 类型
  static propTypes = {
    // 限制 title 必须是字符串
    // isRequired 表示 title 是必传的
    title: PropTypes.string.isRequired,
    // 限制 personInfo 必须是对象，且包含 name 和 age 两个属性
    personInfo: PropTypes.shape({
      // 限制 name 必须是字符串
      name: PropTypes.string,
      // 限制 age 必须是数字
      age: PropTypes.number,
    }),
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
