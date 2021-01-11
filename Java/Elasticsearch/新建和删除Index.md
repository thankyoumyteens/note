# 新建和删除 Index

新建 Index，可以直接向 Elastic 服务器发出 PUT 请求。下面的例子是新建一个名叫weather的 Index。

```
$ curl -X PUT 'localhost:9200/weather'
```

服务器返回一个 JSON 对象，里面的acknowledged字段表示操作成功。

```
{
  "acknowledged":true,
  "shards_acknowledged":true
}
```

然后，我们发出 DELETE 请求，删除这个 Index。

```
$ curl -X DELETE 'localhost:9200/weather'
```
