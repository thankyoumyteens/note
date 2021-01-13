# 索引Index

## 创建索引

创建一个名叫`demo`的索引：

```json
curl -X PUT 'http://localhost:9200/demo'
```

ES响应：

```json
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "demo"
}
```

在创建索引时，可指定主分片和分片副本的数量：

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

ES响应：

```json
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "demo"
}
```

## 查看指定索引

```json
curl -X GET 'http://localhost:9200/demo'
```

ES响应：

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

## 查询ES中的索引

查询ES中索引情况：

```json
curl -X GET 'http://localhost:9200/_cat/indices?v'
```

ES响应：

| health | status | index | uuid | pri | rep | docs.count | docs.deleted | store.size | pri.store.size |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| yellow | open | demo | wqkto5CCTpWNdP3HGpLfxA | 5 | 1 | 0 | 0 | 810b | 810b |
| yellow | open | .kibana | pwKW9hJyRkO7\_pE0MNE05g | 1 | 1 | 1 | 0 | 3.2kb | 3.2kb |

可以看到当前ES中一共有2个索引，一个是我们刚创建的`demo`，另一个是kibana创建的索引`.kibana`。表格中有一些信息代表了索引的一些状态。

health：健康状态，red表示不是所有的主分片都可用，即**部分主分片可用**。yellow表示主分片可用备分片不可用，常常是单机ES的健康状态，greens表示所有的主分片和备分片都可用。（官方对集群健康状态的说明，[https://www.elastic.co/guide/en/elasticsearch/guide/master/cluster-health.html](https://www.elastic.co/guide/en/elasticsearch/guide/master/cluster-health.html)）

status：索引状态，open表示打开可对索引中的文档数据进行读写，close表示关闭此时索引占用的内存会被释放，但是此时索引不可进行读写操作。

index：索引

uuid：索引标识

pri：索引的主分片数量

rep：索引的分片副本数量，1表示有一个分片副本（有多少主分片就有多少备分片，此处表示5个备分片）。

docs.count：文档数量

docs.deleted：被删除的文档数量

store.size：索引大小

pri.store.size：主分片占用的大小

## 删除索引

删除`demo`索引，**删除索引等同于删库跑路，请谨慎操作。**

```json
curl -X DELETE 'http://localhost:9200/demo'
```

ES响应：

```json
{
    "acknowledged": true
}
```

# 类型Type（同时定义映射Mapping字段及类型）

## 创建类型

在前面**基本术语**中我们提到类型Type类似关系型数据库中的表，映射Mapping定义表结构。创建类型Type时需要配合映射Mapping。

创建索引`demo`的类型为`example_type`,包含两个字段：`created`类型为date，`message`类型为keyword：

**方式一：**

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

此时再次执行查询索引的操作，已经可以发现类型Type被创建了，遗憾的是，如果类型Type（或者映射Mapping）一旦定义，就不能删除，只能修改，为了保证本教程顺利进行方式二创建类型，所以此处执行```DELETE http://localhost:9200/demo```删除索引。删除索引后不要再创建索引，下面的这种方式是在创建索引的同时创建Type并定义Mapping

**方式二：**

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

此时执行```GET http://localhost:9200/demo```，可以看到我们在ES中创建了第一个索引以及创建的表结构。
