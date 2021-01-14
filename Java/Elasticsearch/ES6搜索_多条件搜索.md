# 多条件搜索

在ES中表示”与“关系的是关键字```must```，表示”或“关系的是关键字```should```，还有表示表示”非“的关键字```must_not```。

```must```、```should```、```must_not```在ES中称为```bool```查询。

当有多个查询条件进行组合查询时，此时需要上述关键字配合```term```，```match```等。

## 精确查询（```term```，搜索关键字不分词）name="kevin"**且**age="25"的学生。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "bool":{
      "must":[{
        "term":{
          "name.keyword":"kevin"
        }
      },{
        "term":{
          "age":25
        }
      }]
    }
  }
}
```

## 精确查询（```term```，搜索关键字不分词）name="kevin"**或**age="21"的学生。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "bool":{
      "should":[{
        "term":{
          "name.keyword":"kevin"
        }
      },{
        "term":{
          "age":21
        }
      }]
    }
  }
}
```

## 精确查询（```term```，搜索关键字不分词）name!="kevin"**且**age="25"的学生。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "bool":{
      "must":[{
        "term":{
          "age":25
        }
      }],
      "must_not":[{
        "term":{
          "name.keyword":"kevin"
        }
      }]
    }
  }
}
```

如果查询条件中同时包含```must```、```should```、```must_not```，那么它们三者是"且"的关系

多条件查询中查询逻辑(```must```、```should```、```must_not```)与查询精度(```term```、```match```)配合能组合成非常丰富的查询条件。
