# 无条件搜索

```GET http://localhost:9200/user/student/_search?pretty```

查看索引user类型student的数据

# 单条件搜索

ES查询主要分为```term```、```match```。

## term搜索

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "term":{
        "name":"kevin"
    }
  }
}
```

## match搜索

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "match":{
      "name":"kevin"
    }
  }
}
```

## term和match

```term```搜索不会将搜索词进行分词后再搜索, 而```match```则会将搜索词进行分词后再搜索。

如果, 我们对name="kevin yu"进行搜索, 由于```term```搜索不会对搜索词进行搜索, 所以它进行检索的是"kevin yu"这个整体, 而```match```搜索则会对搜索词进行分词搜索, 所以它进行检索的是包含"kevin"和"yu"的数据。

而name字段是```text```类型, 且它是按照```ik_smart```进行分词, "kevin yu"这条数据由于被分词后变成了"kevin"和"yu", 所以```term```搜索不到任何结果。

如果一定要用```term```搜索name="kevin yu", 结果出现"kevin yu", 办法就是在定义映射Mapping时就为该字段设置一个```keyword```类型。

```json
PUT http://localhost:9200/user/student/_mapping
{
  "properties":{
    "name":{
      "type":"text",
      "analyzer":"ik_smart",
      "fields":{
        "keyword":{
          "type":"keyword",
          "ignore_above":256
        }
      }
    },
    "age":{
      "type":"integer"
    }
  }
}
```

重新创建好索引并插入数据后, 再按照```term```搜索keyword="kevin yu"。

```json
POST http://localhost:9200/user/student/_search
{
  "query":{
    "term":{
      "name.keyword":"kevin yu"
    }
  }
}
```

返回一条name="kevin yu"的数据。

## 模糊搜索

```wildcard```通配符查询。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query": {
  "wildcard": {
    "name": "*kevin*"
  }
  }
}
```

## 更智能的模糊搜索

fuzzy也是一个模糊查询。它允许语法错误, 但仍能搜出你想要的结果。例如, 我们查询name等于”kevin“的文档时, 不小心输成了”kevon“, 它仍然能查询出结果。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query": {
  "fuzzy": {
    "name": "kevon"
  }
  }
}
```
