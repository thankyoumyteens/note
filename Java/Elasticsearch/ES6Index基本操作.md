# 索引Index

## 创建索引

创建一个名叫`demo`的索引: 

```json
curl -X PUT 'http://localhost:9200/demo'
```

ES响应: 

```json
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "demo"
}
```

在创建索引时, 可指定主分片和分片副本的数量: 

```json
curl -H 'Content-Type: application/json' -X PUT 'http://localhost:9200/demo' -d '
{
    "settings":{
        "number_of_shards":1,
        "number_of_replicas":1
    }
}
'
```

## 查看指定索引

```json
curl -X GET 'http://localhost:9200/demo'
```

ES响应: 

```json
{
    "demo": {
        "aliases": {},
        "mappings": {},
        "settings": {
            "index": {
                "creation_date": "1561110747038",
                "number_of_shards": "1",
                "number_of_replicas": "1",
                "uuid": "kjPqDUt6TMyywg1P7qgccw",
                "version": {
                    "created": "5060499"
                }, 
                "provided_name": "demo"
            }
        }
    }
}
```

## 查看所有索引

查询ES中索引情况: 

```json
curl -X GET 'http://localhost:9200/_cat/indices?v'
```

ES响应: 

| health | status | index | uuid | pri | rep | docs.count | docs.deleted | store.size | pri.store.size |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| yellow | open | demo | `wqkto5CCTpWNdP3HGpLfxA` | 5 | 1 | 0 | 0 | 810b | 810b |
| yellow | open | .kibana | `pwKW9hJyRkO7\_pE0MNE05g` | 1 | 1 | 1 | 0 | 3.2kb | 3.2kb |


- health: 健康状态, red表示不是所有的主分片都可用。yellow表示主分片可用备分片不可用, 常常是单机ES的健康状态, greens表示所有的主分片和备分片都可用。
- status: 索引状态, open表示打开可对索引中的文档数据进行读写, close表示关闭此时索引占用的内存会被释放, 但是此时索引不可进行读写操作。
- index: 索引
- uuid: 索引标识
- pri: 索引的主分片数量
- rep: 索引的分片副本数量, 1表示有一个分片副本（有多少主分片就有多少备分片, 此处表示5个备分片）。
- docs.count: 文档数量
- docs.deleted: 被删除的文档数量
- store.size: 索引大小
- pri.store.size: 主分片占用的大小

## 删除索引

删除`demo`索引

```json
curl -X DELETE 'http://localhost:9200/demo'
```

# 类型Type

## 创建类型

创建索引`demo`的类型为`example_type`,包含两个字段: `created`类型为date, `message`类型为keyword: 

### 方式一

```json
curl -H 'Content-Type: application/json' -X PUT 'http://localhost:9200/demo/_mapping/example_type' -d '
{
    "properties":{
        "created":{
            "type":"date"
        },
        "message":{
            "type":"keyword"
        }
    }
}
'
```

### 方式二

```json
curl -H 'Content-Type: application/json' -X PUT 'http://localhost:9200/demo' -d '
{
    "mappings":{
        "example_type":{
            "properties":{
                "created":{
                    "type":"date"
                },
                "message":{
                    "type":"keyword"
                }
            }
        }
    }
}
'
```
