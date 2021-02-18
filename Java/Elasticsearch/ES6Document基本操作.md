# 文档Document

## 插入文档

系统自动生成```_id```

```json
curl -H 'Content-Type: application/json' -X POST 'http://localhost:9200/demo/example_type' -d '
{
    "created":1561135459000,
    "message":"test1"
}
'
```

ES响应：

```json
{
    "_index": "demo",
    "_type": "example_type",
    "_id": "AWt67Ql_Tf0FgxupYlBX",
    "_version": 1,
    "result": "created",
    "_shards": {
        "total": 2,
        "successful": 1,
        "failed": 0
    },
    "created": true
}
```

## 查询文档

ElasticSearch的核心功能——搜索。

```POST http://localhost:9200/demo/example_type/_search?pretty```

ES响应：

```json
{
    "took": 183,
    "timed_out": false,
    "_shards": {
        "total": 5,
        "successful": 5,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": 1,
        "max_score": 1,
        "hits": [
            {
                "_index": "demo",
                "_type": "example_type",
                "_id": "AWt67Ql_Tf0FgxupYlBX",
                "_score": 1,
                "_source": {
                    "created": 1561135459000,
                    "message": "test1"
                }
            }
        ]
    }
}
```

## 修改文档

根据文档```_id```修改

```json
POST http://localhost:9200/demo/example_type/AWt67Ql_Tf0FgxupYlBX/_update
{
    "doc":{
        "message":"updated"
    }
}
```

ES响应：

```json
{
    "_index": "demo",
    "_type": "example_type",
    "_id": "AWt67Ql_Tf0FgxupYlBX",
    "_version": 2,
    "result": "updated",
    "_shards": {
        "total": 2,
        "successful": 1,
        "failed": 0
    }
}
```

## 删除文档

删除`_id`为`AWt67Ql\_Tf0FgxupYlBX`的文档

```DELETE http://localhost:9200/demo/example_type/AWt67Ql_Tf0FgxupYlBX```

ES的响应：

```json
{
    "found": true,
    "_index": "demo",
    "_type": "example_type",
    "_id": "AWt67Ql_Tf0FgxupYlBX",
    "_version": 2,
    "result": "deleted",
    "_shards": {
        "total": 2,
        "successful": 1,
        "failed": 0
    }
}
```
