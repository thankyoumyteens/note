# 数据准备

首先创建一个名为user的Index，并创建一个student的Type，Mapping映射一共有如下几个字段：

1. 创建名为user的Index  ```curl -X PUT 'http://localhost:9200/user'```

2. 创建名为student的Type，且指定字段name和address的分词器为```ik_smart```。

```json
curl -H 'Content-Type: application/json' -X POST 'http://localhost:9200/user/student/_mapping' -d '
{
  "properties":{
    "name":{
        "type":"text",
        "analyzer":"ik_smart"
    },
    "age":{
        "type":"short"
    }
  }
}
'
```

插入以下数据。

```json
POST localhost:9200/user/student
{
  "name":"kevin",
  "age":25
}
```

```json
POST localhost:9200/user/student
{
  "name":"kangkang",
  "age":26
}
```

```json
POST localhost:9200/user/student
{
  "name":"mike",
  "age":22
}
```

```json
POST localhost:9200/user/student
{
  "name":"kevin2",
  "age":25
}
```

```json
POST localhost:9200/user/student
{
  "name":"kevin yu",
  "age":21
}
```
