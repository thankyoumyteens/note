# JSX 

JSX 允许 HTML 与 JavaScript 混写

遇到 HTML 标签（以 `<` 开头）, 就用 HTML 规则解析；遇到代码块（以 `{` 开头）, 就用 JavaScript 规则解析。

# jsx语法规则

1. 定义虚拟DOM时, 不要写引号。
2. 标签中混入JS表达式时要用`{}`。
3. 样式的类名指定不要用`class`, 要用`className`。
4. 内联样式, 要用`style={{key:value}}`的形式去写。
5. 只有一个根标签
6. 标签必须闭合
7. 若标签首字母以小写字母开头, 则将该标签转为html中同名元素, 若html中无该标签对应的同名元素, 则报错。
8. 若标签首字母以大写字母开头, react就去渲染对应的组件, 若组件没有定义, 则报错。

## 在 JSX 中嵌入表达式

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

## 给属性赋值

```jsx
const element = <div tabIndex="0"></div>;
const element = <img src={user.avatarUrl}/>;
```
注意: 大括号和引号不能同时出现
