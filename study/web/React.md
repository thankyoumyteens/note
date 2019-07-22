# React组件的互相通信

## 父组件向子组件通信

父组件通过向子组件传递 props，子组件得到 props 后进行相应的处理。

下面是演示代码：

父组件 App.js：

```
import React,{ Component } from "react";
import Child from "./child.js";
import "./App.css";
 
export default class App extends Component{
 
    render(){
        return(
            <div>
                <child title = "今天天气好" />
            </div>
        )
    }
}
```

子组件 child.js：

```
import React from "react";
 
const Child = (props) => {
    return(
        <h1>
            { props.title }
        </h1>
    )
}
 
export default Child;
```

## 子组件向父组件通信

利用回调函数，可以实现子组件向父组件通信：
父组件将一个函数作为 props 传递给子组件，子组件调用该回调函数，
便可以向父组件通信。

下面是演示代码：

Child.js：

```
import React from "react";
 
const Child = (props) => {
    const box = (msg) => {
        return () => {
            props.callback(msg)
        }
    }
    return(
        <div>
            <button onClick = { box("lets_talk") }>点击我</button>
        </div>
    )
}
 
export default Child;
```

App.js：

```
import React,{ Component } from "react";
import Child from "./Child.js";
import "./App.css";
 
export default class App extends Component{
    callback(msg){
        console.log(msg);
    }
    render(){
        return(
            <div>
                <Child callback = { this.callback.bind(this) } />
            </div>
        )
    }
}
```
