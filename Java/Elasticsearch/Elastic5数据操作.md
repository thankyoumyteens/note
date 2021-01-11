#  新增记录

向指定的 `/Index/Type` 发送 PUT 请求, 就可以在 Index 里面新增一条记录。比如, 向`/accounts/person`发送请求, 就可以新增一条人员记录。

```
$ curl -X PUT 'localhost:9200/accounts/person/1' -d '
{
  "user": "张三",
  "title": "工程师",
  "desc": "数据库管理"
}' 
```

服务器返回的 JSON 对象, 会给出 Index、Type、Id、Version 等信息。

```json
{
  "_index":"accounts",
  "_type":"person",
  "_id":"1",
  "_version":1,
  "result":"created",
  "_shards":{"total":2,"successful":1,"failed":0},
  "created":true
}
```

如果你仔细看, 会发现请求路径是`/accounts/person/1`, 最后的1是该条记录的 Id。它不一定是数字, 任意字符串（比如abc）都可以。

新增记录的时候, 也可以不指定 Id, 这时要改成 POST 请求。

```
$ curl -X POST 'localhost:9200/accounts/person' -d '
{
  "user": "李四",
  "title": "工程师",
  "desc": "系统管理"
}'
```

上面代码中, 向`/accounts/person`发出一个 POST 请求, 添加一个记录。这时, 服务器返回的 JSON 对象里面, _id字段就是一个随机字符串。

```json
{
  "_index":"accounts",
  "_type":"person",
  "_id":"AV3qGfrC6jMbsbXb6k1p",
  "_version":1,
  "result":"created",
  "_shards":{"total":2,"successful":1,"failed":0},
  "created":true
}
```

注意, 如果没有先创建 Index（这个例子是accounts）, 直接执行上面的命令, Elastic 也不会报错, 而是直接生成指定的 Index。所以, 打字的时候要小心, 不要写错 Index 的名称。

#  查看记录

向`/Index/Type/Id`发出 GET 请求, 就可以查看这条记录。

```
$ curl 'localhost:9200/accounts/person/1?pretty=true'
```

上面代码请求查看`/accounts/person/1`这条记录, URL 的参数`pretty=true`表示以易读的格式返回。

返回的数据中, found字段表示查询成功, _source字段返回原始记录。

```json
{
  "_index" : "accounts",
  "_type" : "person",
  "_id" : "1",
  "_version" : 1,
  "found" : true,
  "_source" : {
    "user" : "张三",
    "title" : "工程师",
    "desc" : "数据库管理"
  }
}
```

如果 Id 不正确, 就查不到数据, found字段就是false。

```
$ curl 'localhost:9200/weather/beijing/abc?pretty=true'
```

```json
{
  "_index" : "accounts",
  "_type" : "person",
  "_id" : "abc",
  "found" : false
}
```

#  删除记录

删除记录就是发出 DELETE 请求。

```
$ curl -X DELETE 'localhost:9200/accounts/person/1'
```

#  更新记录

更新记录就是使用 PUT 请求, 重新发送一次数据。

```
$ curl -X PUT 'localhost:9200/accounts/person/1' -d '
{
    "user" : "张三",
    "title" : "工程师",
    "desc" : "数据库管理, 软件开发"
}' 
```

```json
{
  "_index":"accounts",
  "_type":"person",
  "_id":"1",
  "_version":2,
  "result":"updated",
  "_shards":{"total":2,"successful":1,"failed":0},
  "created":false
}
```

上面代码中, 我们将原始数据从"数据库管理"改成"数据库管理, 软件开发"。 返回结果里面, 有几个字段发生了变化。


- "_version" : 2,
- "result" : "updated",
- "created" : false

可以看到, 记录的 Id 没变, 但是版本（version）从1变成2, 操作类型（result）从created变成updated, created字段变成false, 因为这次不是新建记录。

# 更新指定的字段

ctx 是单词context的缩写, 表示文档的上下文, 在script中使用ctx引用文档。

```
$ curl -X POST 'localhost:9200/test/type1/1/_update' -d '{
    "script" : {
        "inline": "ctx._source.counter += count",
        "params" : { "count" : 4 }
    },
    "upsert" : { "counter" : 1  }
}'
```

脚本更新文档的字段counter, 把ID为1的文档的counter字段增加4。

upsert参数, 当指定的文档不存在时, upsert参数包含的内容将会被插入到索引中, 作为一个新文档。

例如以下脚本, 当文档存在时, 把文档的counter字段设置为1；当文档不存在时, 插入一个新的文档, 文档的counter字段的值是2。

```
{  
   "script":{  
      "inline":"ctx._source.counter= 1"
   },
   "upsert":{"counter":2}
}
```

