# 三种状态:

1.  Pending(进行中)
2.  Fulfilled(已完成)
3.  Rejected(已失败)

Promise 对象的状态改变，只有两种可能: 从 Pending 变为 Fulfilled 和从 Pending 变为 Rejected。只要这两种情况发生，状态就不会再变了

# 常用方法

- Promise.all

Promise.all 可以将多个 Promise 实例包装成一个新的 Promise 实例。成功的时候返回(等到所有 Promise 完成后才返回)的是一个结果数组，失败的时候则返回最先被 reject 失败状态的值。

```
let p1 = new Promise((resolve, reject) => {
    resolve('p1')
})

let p2 = new Promise((resolve, reject) => {
    resolve('p2')
})

Promise.all([p1, p2]).then((result) => {
    console.log(result) // ['p1', 'p2']
})
```

- Promise.race

返回最先完成的结果，不管结果本身是成功状态还是失败状态。


# 回调地狱

```
fs.readFile('./sample.txt', 'utf-8', (err, content) => {
    let keyword = content.substring(0, 5);
    db.find(`select * from sample where kw = ${keyword}`, (err, res) => {
        get(`/sampleget?count=${res.length}`, data => {
           console.log(data);
        });
    });
});
```

每增加一个异步请求，就会多添加一层回调函数的嵌套，这段代码中三个异步函数的嵌套已经开始使一段本可以语言明确的代码编程不易阅读与维护了。

左侧明显出现了一个三角形的缩进区域，过多的回调也就让我们陷入“回调地狱”。

# Promise 解决回调地狱

嵌套操作变成了通过 then 连接的链式操作。代码的整洁度上有了一个较大的提高。

```
function getData(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(url.replace('url', 'data'))
        }, 1000)
    })
}

function doTest() {
    getData('url_111').then(data => {
        console.log(data)
        // getData('url_222').then(data => {
        //     console.log(data)
        // })
        return getData('url_222')
    }).then(data => {
        console.log(data)
        return getData('url_333')
    }).then(data => {
        console.log(data)
    })
}

doTest()
```
