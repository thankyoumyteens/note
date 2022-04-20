方法1
```js
new Vue({
    el:'#demo',
    data:{
        address:'北京'
    }
})
```

方法2
```js
new Vue({
    data:{
        address:'北京'
    }
}).$mount('#demo');
```
