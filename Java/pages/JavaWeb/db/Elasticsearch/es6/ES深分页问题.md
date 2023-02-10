# from + size 的问题

es 默认采用的分页方式是 from+ size 的形式，在深度分页的情况下，这种使用方式效率是非常低的，比如如下查询
```
GET /student/student/_search
{
  "query":{
    "match_all": {}
  },
  "from":5000,
  "size":10
}
```
意味着 es 需要在各个分片上匹配排序并得到5010条数据，协调节点拿到这些数据再进行排序等处理，然后结果集中取最后10条数据返回。

es为了性能，限制了分页的深度，es目前支持的最大的 max_result_window = 10000；也就是说不能分页到10000条数据以上。 

# scroll 分页

使用scroll滚动搜索，可以先搜索一批数据，然后下次再搜索一批数据，以此类推，直到搜索出全部的数据

scroll搜索会在第一次搜索的时候，保存一个当时的搜索上下文，之后只会基于该旧的搜索上下文提供数据搜索，如果这个期间数据变更，是不会让用户看到的。

执行如下curl，每次请求两条。可以定制 scroll = 5m意味着搜索上下文过期时间为5分钟。
```
GET /student/student/_search?scroll=5m
{
  "query": {
    "match_all": {}
  },
  "size": 2
}
```
在返回结果中，有一个`_scroll_id`字段

在后面的请求中我们都要带着这个 scroll_id 去请求。在获取下一个批量的结果时候，不需要指定index和type。

```
GET /_search/scroll
{
  "scroll":"5m",
  "scroll_id":"xxx"
}
```

搜索上下文在 scroll 超时就会自动移除。但是保持 scroll 存活需要代价，所以 当scroll不再被使用的时候可以通过 clear-scroll 显式地清除：

```
DELETE /_search/scroll
{
    "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
}
```
可以通过传递All参数，删除当前存在的所有Scroll。
```
DELETE /_search/scroll/_all
```

# search_after 分页

search_after 是一种假分页方式，根据上一页的最后一条数据来确定下一页的位置，同时在分页请求的过程中，如果有索引数据的增删改查，这些变更也会实时的反映到游标上。为了找到每一页最后一条数据，每个文档必须有一个全局唯一值，官方推荐使用 _uid 作为全局唯一值，但是只要能表示其唯一性就可以。

```
GET /student/student/_search
{
  "query":{
    "match_all": {}
  },
  "size":10,
  "search_after":[1005], // 上一页最后一条数据的uid=1005
  "sort":[
    {
      "uid": "desc"
    }
  ]
}
```
