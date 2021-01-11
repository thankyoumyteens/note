# 返回所有记录

使用 GET 方法，直接请求`/Index/Type/_search`，就会返回所有记录。

```
$ curl 'localhost:9200/accounts/person/_search'
```

```json
{
  "took":2,
  "timed_out":false,
  "_shards":{"total":5,"successful":5,"failed":0},
  "hits":{
    "total":2,
    "max_score":1.0,
    "hits":[
      {
        "_index":"accounts",
        "_type":"person",
        "_id":"AV3qGfrC6jMbsbXb6k1p",
        "_score":1.0,
        "_source": {
          "user": "李四",
          "title": "工程师",
          "desc": "系统管理"
        }
      },
      {
        "_index":"accounts",
        "_type":"person",
        "_id":"1",
        "_score":1.0,
        "_source": {
          "user" : "张三",
          "title" : "工程师",
          "desc" : "数据库管理，软件开发"
        }
      }
    ]
  }
}
```

上面代码中，返回结果的 took字段表示该操作的耗时（单位为毫秒），timed_out字段表示是否超时，hits字段表示命中的记录，里面子字段的含义如下。

- total：返回记录数，本例是2条。
- max_score：最高的匹配程度，本例是1.0。
- hits：返回的记录组成的数组。

返回的记录中，每条记录都有一个_score字段，表示匹配的程序，默认是按照这个字段降序排列。

# 全文搜索

Elastic 的查询非常特别，使用自己的查询语法，要求 GET 请求带有数据体。

```
$ curl 'localhost:9200/accounts/person/_search'  -d '
{
  "query" : { "match" : { "desc" : "软件" }}
}'
```

上面代码使用 Match 查询，指定的匹配条件是desc字段里面包含"软件"这个词。返回结果如下。

```json
{
  "took":3,
  "timed_out":false,
  "_shards":{"total":5,"successful":5,"failed":0},
  "hits":{
    "total":1,
    "max_score":0.28582606,
    "hits":[
      {
        "_index":"accounts",
        "_type":"person",
        "_id":"1",
        "_score":0.28582606,
        "_source": {
          "user" : "张三",
          "title" : "工程师",
          "desc" : "数据库管理，软件开发"
        }
      }
    ]
  }
}
```

Elastic 默认一次返回10条结果，可以通过size字段改变这个设置。

```
$ curl 'localhost:9200/accounts/person/_search'  -d '
{
  "query" : { "match" : { "desc" : "管理" }},
  "size": 1
}'
```

上面代码指定，每次只返回一条结果。

还可以通过from字段，指定位移。

```
$ curl 'localhost:9200/accounts/person/_search'  -d '
{
  "query" : { "match" : { "desc" : "管理" }},
  "from": 1,
  "size": 1
}'
```

上面代码指定，从位置1开始（默认是从位置0开始），只返回一条结果。

# 逻辑运算

如果有多个搜索关键字， Elastic 认为它们是or关系。

```
$ curl 'localhost:9200/accounts/person/_search'  -d '
{
  "query" : { "match" : { "desc" : "软件 系统" }}
}'
```

上面代码搜索的是软件 or 系统。

如果要执行多个关键词的and搜索，必须使用布尔查询。

```
$ curl 'localhost:9200/accounts/person/_search'  -d '
{
  "query": {
    "bool": {
      "must": [
        { "match": { "desc": "软件" } },
        { "match": { "desc": "系统" } }
      ]
    }
  }
}'
```

# URI搜索

请求参数位于_search端点之后, 参数之间使用&分割, 例如: 
```
GET /_search?pretty&q=title:azure&explain=true&from=1&size=10&sort=title:asc&fields:user,title,content
```

## pretty参数

默认情况下, API返回的JSON对象忽略换行符, 在请求中加上pretty参数, 使返回的结果集JSON可读。

## q参数

q参数用于指定查询条件, 例如: `q=title:azure`, 指定搜索title字段中包含azure关键字的文档

- 一个字段包含多个关键字, 关键字之间使用空格或逗号分隔, 例如: `q=title:(azure,aws,cloud)`, 或 `q=title:(azure aws cloud)`, 指定搜索title字段中包含azure, aws或cloud的文档
- 搜索短语使用双引号标识, 例如: q=title:"azure vs aws", 指定搜索title中包含短语“azure vs aws”的文档
- 指定操作符: +或-, 操作符 + 用于指定返回的文档必须匹配查询条件；操作符 - 用于指定返回的文档不匹配查询条件；操作符之间以空格分隔, 操作符是位于查询条件=号右侧, 字段前面, 例如 `q=+title:azure -title:aws`, 指定搜索字段title中只能包含azure, 不能包含aws；

## default_operator参数

在API中可以包含多个查询条件q, 默认条件下, 多个查询条件之间的关系是or关系, 例如: `q=title:azure&q=content:azure`, 指定搜索title字段中包含azure关键字, 或者content字段中包含azure关键字的文档。

查询条件之间的逻辑关系由default_operator参数指定, 默认值是or, 该属性可以设置为and 或 or:

- 设置为or, 例如: `q=title:azure&q=content:azure&default_operator=or`
- 设置为and, 例如: `q=title:azure&q=content:azure&default_operator=and`

## fields参数

默认情况下, 返回的每个文档都包括_index,_type,_id,_score和_source字段, fields 用于指定返回的字段列表。在查询时, 通过fields参数, 指定一个以逗号分隔的字段列表, 这些字段的store属性必须设置为true, 或存在于_source字段中。默认情况下, fields字段的参数值是_source。可以指定一个或多个字段, 字段之间以逗号分隔: 
`fields=title`或`fields=title,user`

## sort参数

sort参数用于对结果进行排序, 使ElasticSearch按照指定的字段对结果进行排序, 值是`fieldName:asc/fieldName:desc`, 默认是升序排序, 可以有多个排序字段, 排序字段之间以逗号分割, 例如: `sort=field1:asc,field:desc`

## 其他参数

- explain参数: 设置为true时, ElasticSearch将在结果中的文档中包含额外的解释信息；
- from参数: from参数指定结果从哪个记录开始返回, 默认值是0；
- size参数: 定义了返回结果的最大文档数量, 默认值是10, 参数示例: from=10&size=15
- lowercase_expanded_terms参数: 自动将词条转换成小写, 默认值是true；
- analyze_wildcard参数: 通配符或前缀是否被分析, 默认值是false；
