# URI搜索

请求参数位于_search端点之后, 参数之间使用&分割, 例如: 
```
GET /_search?pretty&q=title:azure&explain=true&from=1&size=10&sort=title:asc&fields:user,title,content
```

## pretty参数

默认情况下, API返回的JSON对象忽略换行符, 在请求(Request)中加上pretty参数, 强制ElasticSearch引擎在响应(Response)中加上换行符, 使返回的结果集JSON可读。

## 查询条件(q)参数

q参数用于指定返回的文档必须匹配的查询条件, 例如: `q=title:azure`, 指定搜索title字段中包含azure关键字的文档；

可以设置一个字段包含多个关键字, 关键字之间使用空格或逗号分隔, 例如: `q=title:(azure,aws,cloud)`, 或 `q=title:(azure aws cloud)`, 指定搜索title字段中包含azure, aws或cloud的文档；只要title字段包含任意一个关键字, 文档就满足查询条件；

q参数可以指定搜素一个短语, 短语使用双引号标识, 例如: q=title:"azure vs aws", 指定搜索title中包含短语“azure vs aws”的文档；

在查询条件中, 也可以指定操作符: +或-, 操作符 + 用于指定返回的文档必须匹配查询条件；操作符 - 用于指定返回的文档不匹配查询条件；操作符之间以空格分隔, 操作符是位于查询条件=号右侧, 字段前面, 例如 `q=+title:azure -title:aws`, 指定搜索字段title中只能包含azure, 不能包含aws；

## 默认操作符(default_operator)参数

在API中可以包含多个查询条件q, 默认条件下, 多个查询条件之间的关系是or关系, 例如: `q=title:azure&q=content:azure`, 指定搜索title字段中包含azure关键字, 或者content字段中包含azure关键字的文档。

查询条件之间的逻辑关系由default_operator参数指定, 默认值是or, 该属性可以设置为and 或 or；

- 当设置为or时, 只要一个查询条件(q)满足, 就返回文档；例如: `q=title:azure&q=content:azure&default_operator=or`
- 当设置为and时, 所有的查询条件都满足时, 才返回文档；例如: `q=title:azure&q=content:azure&default_operator=and`

对于查询: `q=title:(azure,aws)&q=content:(azure,aws)`, 表示搜索文档的字段title或content, 只要字段值中出现azure 或 aws关键字, 就表示该文档匹配查询条件, 作为查询结果返回。

## 投影字段(fields)参数

默认情况下, 返回的每个文档都包括_index,_type,_id,_score和_source字段, fields 用于指定返回的字段列表。在查询时, 通过fields参数, 指定一个以逗号分隔的字段列表, 这些字段的store属性必须设置为true, 或存在于_source字段中。默认情况下, fields字段的参数值是_source。可以指定一个或多个字段, 字段之间以逗号分隔: 
`fields=title`或`fields=title,user`

## 排序(sort)参数

sort参数用于对结果进行排序, 使ElasticSearch按照指定的字段对结果进行排序, 值是`fieldName:asc/fieldName:desc`, 默认是升序排序, 可以有多个排序字段, 排序字段之间以逗号分割, 例如: `sort=field1:asc,field:desc`

## 其他参数

- 解释(explain)参数: 设置为true时, ElasticSearch将在结果中的文档中包含额外的解释信息；
- 分页(from和size)参数: 用于指定结果窗口, from参数指定结果从哪个记录开始返回, 默认值是0；
- size参数: 定义了返回结果的最大文档数量, 默认值是10, 参数示例: from=10&size=15
- 小写词条(lowercase_expanded_terms)参数: 自动将词条转换成小写, 默认值是true；
- 分析通配符(analyze_wildcard)参数: 通配符或前缀是否被分析, 默认值是false；

# 查询请求

搜索API可以转换为查询请求, 如下代码, 查询请求的查询条件是词条查询, 查询参数和URI搜索的参数是对应的: 

```
GET /_search -d 
{  
   "from":0,
   "size":10,
   "sort":[  
      {"post_date":{"order":"asc"}},
      { "name":"desc" }
   ],
   "fields":[ "name","postDate","age"],
   "query":{  
      "term":{ "user":"kimchy"}
   }
}
```

# 查询条件

在查询条件结点"query"中, 指定查询的类型是词条(Term), 在词条中指定查询的条件, 例如, 只要User中包含kimchy关键字, 就满足查询条件: 

```json
"query" : {
    "term" : { "user" : "kimchy" }
}
```

## 排序

排序sort字段指定排序的字段及其排序的方向, 并且排序值(Sort Value)作为查询结果返回: 

```json
"sort":[  
   {   "post_date":{   "order":"asc" }},
   {   "name":"desc"  }
]
```

排序的方向: 升序asc, 降序desc, 对于_score字段, 默认的排序方式是降序desc, 对于其他字段, 默认的排序方向是asc。

当对字符串字段进行排序时, 该字段最好不被分词(analyzed或tokenized), 如果字符串字段被分析, 那么ElasticSearch引擎将随机选取字段的一个分词(Term)进行排序, 这可能不是你想要的排序值。

# 投影, 选取返回的字段

投影字段(fields), 用来限制返回的字段, 该字段必须存储在倒排索引中, 也就是说, 在索引映射中, 该字段的store属性为ture。推荐使用_source字段, 从文档源数据中, 指定需要返回的字段。示例, 使用_source 字段, 控制结果hits数组中, 每个文档_source字段必须返回的字段: 

```json
{
    "_source": {
        "include": [ "filed1", "field2" ],
        "exclude": [ "field3" ]
    },
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}
```

# 窗口字段

窗口字段 from 和 size, 用来限制返回的文档数量
