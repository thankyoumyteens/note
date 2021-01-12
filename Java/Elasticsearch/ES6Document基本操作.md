# 新建document

在index为customer, type为_doc下新建一个id=1的document
```
curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/customer/_doc/1?pretty' -d '
{
  "name": "John Doe"
}
'
```

```json
{
  "_index" : "customer",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}
```

# 获取document

```
curl -X GET 'localhost:9200/customer/_doc/1?pretty'
```

```json
{
  "_index" : "customer",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "found" : true,
  "_source" : {
    "name" : "John Doe"
  }
}
```

# 修改document

Elasticsearch的更新是删除原文档后再创建新文档

修改现有字段
```
curl -H 'Content-Type: application/json' -X POST 'localhost:9200/customer/_doc/1/_update?pretty' -d '
{
  "doc": { "name": "Jane Doe" }
}
'
```

增加新字段
```
curl -H 'Content-Type: application/json' -X POST 'localhost:9200/customer/_doc/1/_update?pretty' -d '
{
  "doc": { "name": "Jane Doe", "age": 20 }
}
'
```

使用脚本把age字段加5
```
curl -H 'Content-Type: application/json' -X POST 'localhost:9200/customer/_doc/1/_update?pretty' -d '
{
  "script" : "ctx._source.age += 5"
}
'
```

# 删除document

```
curl -X DELETE 'localhost:9200/customer/_doc/1?pretty'
```

# 批量操作

一次请求创建两个文档(ID 1 - John Doe 和 ID 2 - Jane Doe)
```
curl -H 'Content-Type: application/json' -X POST 'localhost:9200/customer/_doc/_bulk?pretty' -d '
{"index":{"_id":"1"}}
{"name": "John Doe" }
{"index":{"_id":"2"}}
{"name": "Jane Doe" }
'
```

一次请求更新ID1的文档并删除ID2的文档
```
curl -H 'Content-Type: application/json' -X POST 'localhost:9200/customer/_doc/_bulk?pretty' -d '
{"update":{"_id":"1"}}
{"doc": { "name": "John Doe becomes Jane Doe" } }
{"delete":{"_id":"2"}}
'
```
