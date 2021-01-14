# 无条件搜索

```GET http://localhost:9200/user/student/_search?pretty```

查看索引user的student类型数据，得到刚刚插入的数据

# 单条件搜索

ES查询主要分为```term```、```match```。

## term搜索

我们用```term```搜索name为“kevin”的数据。

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

搜索结果出现了两条数据：name="kevin"和name="keivin yu"。

## match搜索

同样，搜索name为“kevin”的数据。

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

```match```的搜索结果竟然仍然是两条数据：name="kevin"和name="keivin yu"。

## term和match

**```term```搜索不会将搜索词进行分词后再搜索，而```match```则会将搜索词进行分词后再搜索**。

如果，我们对name="kevin yu"进行搜索，由于```term```搜索不会对搜索词进行搜索，所以它进行检索的是"kevin yu"这个整体，而```match```搜索则会对搜索词进行分词搜索，所以它进行检索的是包含"kevin"和"yu"的数据。而name字段是```text```类型，且它是按照```ik_smart```进行分词，"kevin yu"这条数据由于被分词后变成了"kevin"和"yu"，所以```term```搜索不到任何结果。

如果一定要用```term```搜索name="kevin yu"，结果出现"kevin yu"，办法就是在定义映射Mapping时就为该字段设置一个```keyword```类型。

删除```DELETE http:localhost:9200/user/student```重新按照开头创建索引以及插入数据。

唯一需要修改的是在定义映射Mapping时，name字段修改为如下所示：

```json
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

待我们重新创建好索引并插入数据后，此时再按照```term```搜索name="kevin yu"。

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

返回一条name="kevin yu"的数据。按照```match```搜索同样出现name="kevin yu"，因为name.keyword无论如何都不会再分词。

_在已经建立索引且定义好映射Mapping的情况下，如果直接修改name字段，此时能修改成功，但是却无法进行查询，这与ES底层实现有关，如果一定要修改要么是新增字段，要么是重建索引。_

## 类似like的模糊搜索

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

ES返回结果包括name="kevin"，name="kevin2"，name="kevin yu"。

## fuzzy更智能的模糊搜索

fuzzy也是一个模糊查询，它看起来更加”智能“。它类似于搜狗输入法中允许语法错误，但仍能搜出你想要的结果。例如，我们查询name等于”kevin“的文档时，不小心输成了”kevon“，它仍然能查询出结构。

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

ES返回结果包括name="kevin"，name="kevin yu"。
