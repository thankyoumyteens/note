# 分页搜索

ES分页查询包含```from```和```size```关键字, ```from```表示第几页, ```size```表示每页的大小。

使用```sort```关键字指定排序字段以及降序升序。

## 分页（一页包含1条数据）查询age >= 21且age <=26的学生, 按年龄降序排列。

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

ES默认升序排列, 如果不指定排序字段的排序）, 则```sort```字段可直接写为```"sort":"age"```。
