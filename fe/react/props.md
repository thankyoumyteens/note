# props

通常props扮演着数据传递的角色

props是只读的

# 在函数组件之中传递

```jsx
//props基本使用
function Com(props){
    return (
        <div>外部传递的数据：{props.text} ---{props.num}</div>
    )
}

//使用对象进行传递多个数据
let obj={
    text:"text数据",
    num:"num数据"
}

//...是ES6的扩展运算符 
// 用于取出参数对象中的所有可遍历属性，拷贝到当前对象之中
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
            <div>外部传递的数据：{props.text} ---{props.num}</div>
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
            <div>外部传递的数据：{props.text} ---{props.num}</div>
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
            <div>外部传递的数据：{props.text} ---{props.num}</div>
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
