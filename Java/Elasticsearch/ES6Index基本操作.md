# 新建 Index

新建 Index，可以直接向 Elastic 服务器发出 PUT 请求

下面的例子是新建一个名叫 customer 的 Index, pretty 标识返回格式化的json
```
curl -X PUT 'localhost:9200/customer?pretty'
```

服务器返回一个 JSON 对象，里面的acknowledged字段表示操作成功。
```json
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "customer"
}
```

# 查看所有的index

```
curl -X GET 'localhost:9200/_cat/indices?v'
```

```
health status index    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   customer rrtTK4ZzRVSG3LOAZD_-yg   5   1          0            0      1.1kb          1.1kb
```


# 删除 Index

```
curl -X DELETE 'localhost:9200/customer?pretty'
```

```json
{
  "acknowledged" : true
}
```
