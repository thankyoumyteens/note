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

不存在查询顾名思义查询不存在某个字段的数据。在以前ES有```missing```表示查询不存在的字段，后来的版本中由于```must not```和```exists```可以组合成```missing```，故去掉了```missing```。

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
