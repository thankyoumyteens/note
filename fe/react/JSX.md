# JSX 

JSX 允许 HTML 与 JavaScript 混写

遇到 HTML 标签（以 `<` 开头），就用 HTML 规则解析；遇到代码块（以 `{` 开头），就用 JavaScript 规则解析。

# 在 JSX 中嵌入表达式

可以在大括号内放置任何有效的 JavaScript 表达式。例如, `2 + 2`, `user.firstName` 或 `formatName(user)` 都是有效的 JavaScript 表达式。

建议将jsx内容包裹在括号中, 但不必须

```jsx
function formatName(user) {
  return user.firstName + ' ' + user.lastName;
}

const user = {
  firstName: 'Harper',
  lastName: 'Perez'
};

const element = (
  <h1>
    Hello, {formatName(user)}!
  </h1>
);

ReactDOM.render(
  element,
  document.getElementById('root')
);
```

# 使用JSX表达式

可以在 if 语句和 for 循环的代码块中使用 JSX, 将 JSX 赋值给变量, 把 JSX 当作参数传入, 以及从函数中返回 JSX: 

```jsx
function getGreeting(user) {
  if (user) {
    return <h1>Hello, {formatName(user)}!</h1>;
  }
  return <h1>Hello, Stranger.</h1>;
}
```

# 给属性赋值

可以通过使用引号, 来将属性值指定为字符串字面量。也可以使用大括号, 来在属性值中插入一个 JavaScript 表达式

```jsx
const element = <div tabIndex="0"></div>;
const element = <img src={user.avatarUrl}/>;
```

注意: 大括号和引号不能同时出现

# 

Babel 会把 JSX 转译成一个名为 React.createElement() 函数调用。

```jsx
const element = (
  <h1 className="greeting">
    Hello, world!
  </h1>
);
// 等价于:
const element = React.createElement(
  'h1',
  {className: 'greeting'},
  'Hello, world!'
);
```
React.createElement() 会预先执行一些检查, 它实际上创建了一个这样的对象: 
```jsx
// 注意: 这是简化过的结构
const element = {
  type: 'h1',
  props: {
    className: 'greeting',
    children: 'Hello, world!'
  }
};
```
