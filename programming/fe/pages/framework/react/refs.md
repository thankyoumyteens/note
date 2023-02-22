# 什么是Refs

Refs其实是提供了一个对真实DOM/组件的引用，我们可以通过这个引用直接去操作DOM/组件

# 设置refs

## 方式1 字符串形式

官网不推荐使用这种形式使用refs了，并且这种方法在未来的版本可能会被移除。

```jsx
class MyComponent extends React.Component {
    handleClick() {
        // 使用原生的 DOM API 获取焦点
        this.refs.myInput.focus();
    }
    render() {
        // 当组件插入到 DOM 后，ref 属性添加一个组件的引用于到 this.refs
        return (
            <div>
                <input type="text" ref="myInput" />
                <button onClick={this.handleClick.bind(this)}/>点我输入框获取焦点</button>
            </div>
        );
    }
}
```

## 方式2 回调函数形式

```jsx
class CustomTextInput extends React.Component {
    constructor(props) {
        super(props);
        this.textInput = React.createRef();
    }

    handleClick() {
        this.textInput.current.focus();
    }

    render() {
        return (
            <div>
                <input type="text" ref={this.textInput} />
                <button onClick={this.handleClick.bind(this)}/>点我输入框获取焦点</button>
            </div>
        );
    }
}
```

current属性

- 如果ref属性被用于html元素，那么它的值是底层DOM元素。
- 如果ref属性被用于自定义类组件，那么它的值是已挂载的这个自定义类组件的实例。
- 函数式组件没有ref属性。

### 指定回调函数

```jsx
class CustomTextInput extends React.Component {
    constructor(props) {
        super(props);
        this.textInput = React.createRef();
    }

    test(element) {
        console.log()
        this.textInput = element
    }

    handleClick() {
        this.textInput.current.focus();
    }

    render() {
        return (
            <div>
                <input type="text" ref={this.test} />
                <button onClick={this.handleClick.bind(this)}/>点我输入框获取焦点</button>
           </div>
        );
    }
}
```

# 通过ref调用子组件的方法

子组件
```jsx
class CustomInput extends Component {
    constructor(props) {
        super(props);
        this.handleFocus = this.handleFocus.bind(this);
        this.myRef = React.createRef();
    }

    handleFocus(e) {
        this.myRef.current.focus();
    }
    render() {
        return(
            <input type="text" ref={this.myRef}/>
        )
    }

}
```
父组件
```jsx
class NoControl extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.myRef = React.createRef();
    }
    handleSubmit(e) {
        e.preventDefault();
        this.myRef.current.handleFocus();
    }

    render() {
        return(
            <form onSubmit={this.handleSubmit}>
                <CustomInput ref={this.myRef}/>
                <button type="submit">Submit</button>
            </form>
        );
    }
}
```
