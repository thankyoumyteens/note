# JSX

JSX 允许 HTML 与 JavaScript 混写

遇到 HTML 标签(以 `<` 开头), 就用 HTML 规则解析。遇到代码块(以 `{` 开头), 就用 JavaScript 规则解析。

jsx 语法规则:

1. 标签中混入 JS 表达式时要用 `{}` 包起来
   ```jsx
   function MyApp() {
     return <h1>Hello, world!</h1>;
   }
   ```
2. 样式的类名指定不要用 class，要用 className
   ```jsx
   function MyApp() {
     return <h1 className="big-font">Hello, world!</h1>;
   }
   ```
3. 内联样式，要用 `style={{key:value}}`的形式
   ```jsx
   function MyApp() {
     return <h1 style={{ fontSize: "100px" }}>Hello, world!</h1>;
   }
   ```
4. 只能有一个根标签
5. 标签必须闭合
6. 标签首字母
   - 若小写字母开头，则将标签转为 htm1 中同名元素
   - 若大写字母开头，则视为组件
