# 分页搜索

ES分页查询包含```from```和```size```关键字，```from```表示起始值，```size```表示一次查询的数量。

## 分页（一页包含1条数据）模糊查询(```match```，搜索关键字不分词)name="kevin"

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "match":{
      "name":"kevin"
    }
  },
  "from":0,
  "size":1
}
```

分页查询中往往我们也需要对数据进行排序返回，MySQL中使用```order by```关键字，ES中使用```sort```关键字指定排序字段以及降序升序。

## 分页（一页包含1条数据）查询age >= 21且age <=26的学生，按年龄降序排列。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "range":{
      "age":{
        "gte":21,
        "lte":26
      }
    }
  },
  "from":0,
  "size":1,
  "sort":{
    "age":{
      "order":"desc"
    }
  }
}
```

ES默认升序排列，如果不指定排序字段的排序），则```sort```字段可直接写为```"sort":"age"```。
