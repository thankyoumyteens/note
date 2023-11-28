# props

通常props扮演着数据传递的角色

props是只读的

# 在函数组件之中传递

```jsx
//props基本使用
function Com(props){
    return (
        <div>外部传递的数据: {props.text} ---{props.num}</div>
    )
}

//使用对象进行传递多个数据
let obj={
    text:"text数据",
    num:"num数据"
}

//...是React的语法, 把obj展开后传入子组件, 只能用在此处
ReactDOM.render(
    <Com {...obj} />,
    document.getElementById("demoReact")
);    
```

# 在类组件之中传递

```jsx
//使用对象进行传递多个数据
let obj={
    text:"text数据",
    num:"num数据"
}
//类组件
class Com extends React.Component{
    render(){
        return(
            <div>外部传递的数据: {props.text} ---{props.num}</div>
        )
    }
}
ReactDOM.render(
    <Com {...obj} />,
    document.getElementById("demoReact")
);  
```

# props默认值

## 方法1

```jsx
//使用对象进行传递多个数据
let obj={
    text:"text数据",
    num:"num数据"
}
//类组件
class Com extends React.Component{
    static defaultProps = { 
        text:"默认text数据",
        num:"默认num数据"
    }
    render(){
        return(
            <div>外部传递的数据: {props.text} ---{props.num}</div>
        )
    }
}
ReactDOM.render(
    <Com {...obj} />,
    document.getElementById("demoReact")
);  
```

## 方法2

```jsx
//使用对象进行传递多个数据
let obj={
    text:"text数据",
    num:"num数据"
}
//类组件
class Com extends React.Component{
    render(){
        return(
            <div>外部传递的数据: {props.text} ---{props.num}</div>
        )
    }
}

Com.defaultProps = { 
    text:"默认text数据",
    num:"默认num数据"
}

ReactDOM.render(
    <Com {...obj} />,
    document.getElementById("demoReact")
);  
```

# props数据类型限制

需要引入`prop-types.js`

```jsx
class Com extends React.Component{
    static propTypes = {
        // text是string类型且必传
        text: PropTypes.string.isRequired,
        // num是number类型且非必传
        num: PropTypes.number,
    }

    render(){
        return(
            <div>外部传递的数据: {props.text} ---{props.num}</div>
        )
    }
}
```

PropTypes的取值
- `PropTypes.array` 数组
- `PropTypes.bool` 布尔
- `PropTypes.func` 函数
- `PropTypes.number` 数字
- `PropTypes.object` 对象
- `PropTypes.string` 字符串
- `PropTypes.symbol` ES6新增的symbol类型
