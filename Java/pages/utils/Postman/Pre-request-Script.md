# 通过Pre-request Script设置请求携带Token

```js
// 获取environment中的属性
var localhostUrl = pm.environment.get('localhostUrl')
var tokenUrl = {
    url: 'http://' + localhostUrl + '/oauth/token',
    method: 'POST',
    header: 'Content-Type: application/json',
    body: {
        mode: 'raw',
        raw: JSON.stringify({ "account": "uid", "password": "pwd" })
    }
}
pm.sendRequest(tokenUrl, function (err, response) {
    var jData = response.json();
    // 设置environment中的属性
    pm.environment.set("Auth", 'bearer ' + jData.item.access_token);
});
```
