# 实现方式

服务端以 content-type: ‘application/octet-stream’ 的格式返回前端, 前端接收到数据后使用 Blob 来接收数据, 并且创建a标签进行下载。

# 后端

```js
// 这里以express举例
const fs = require('fs')
const express = require('express')
const bodyParser = require('body-parser')

const app = express()
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())

// 以post提交举例
app.post('/info/download', function(req, res) {
    const filePath = './myfile/test.zip'
    const fileName = 'test.zip'
    
    res.set({
        'content-type': 'application/octet-stream',
        'content-disposition': 'attachment;filename=' + encodeURI(fileName)
    })

    fs.createReadStream(filePath).pipe(res)
})

app.listen(3000)
```

# 前端

```js
axios.post(url, {...params}, {responseType: 'blob'})
    .then((res) => {
        const { data, headers } = res
        const fileName = headers['content-disposition'].replace(/\w+;filename=(.*)/, '$1')
        // new Blob(array,options)
        // 第一个参数为一个数组, 为需要被处理的数据, 第二个参数为配置参数, 一般填上该数据的mime类型
        const blob = new Blob([data], {type: headers['content-type']})
        let dom = document.createElement('a')
        let url = window.URL.createObjectURL(blob)
        dom.href = url
        dom.download = decodeURI(fileName)
        dom.style.display = 'none'
        document.body.appendChild(dom)
        dom.click()
        dom.parentNode.removeChild(dom)
        window.URL.revokeObjectURL(url)
    }).catch((err) => {})
```

# 下载Excel报格式错误而且乱码问题

原因: 使用了mockjs, 导致了Request类型被封装, mock会拦截所有的请求, 匹配规则的就使用模拟数据, 不匹配的也会使用封装后的request请求后台

解决: 测试下载文件时去掉mock引入
