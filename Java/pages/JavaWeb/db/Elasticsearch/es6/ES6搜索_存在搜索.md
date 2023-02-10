# 存在查询

查询存在name字段的数据。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "exists":{
      "field":"name"
    }  
  }
}
```

# 不存在查询

查询不存在name字段的数据。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "bool":{
      "must_not":{
        "exists":{
          "field":"name"
        }
      }
    }  
  }
}
```
