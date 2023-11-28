# term和match的区别

- term是完全匹配, 搜索前不会对搜索词进行分词
- match进行搜索时, 会先进行分词拆分, 拆完后再匹配
- 应该避免使用term去查询属性类型为text的属性, 因为类型为text的字段在存储时会被分词处理

# 单条trem查询

POST请求 localhost:9200/nba/_search

请求体
```json
{
    // 查询jerse_no==23的文档
    "query": { // 查询
        "term": { // 词条
            "jerse_no": "23" // 字段名称
        }
    }
}
```

# 多条trem查询

POST请求 localhost:9200/nba/_search

请求体
```json
{
    // 查询jerse_no==23或jerse_no==13的文档
    "query": {
        "terms": {
            "jerse_no": ["23", "13"]
        }
    }
}
```

# 查询全部

POST请求 localhost:9200/nba/_search

请求体
```json
{
    "query": {
        // 查询全部文档, 默认显示10条记录
        "match_all": {}
    },
    "from": 0, // 从0开始
    "size": 100 // 查询100条
}
```

# match查询

POST请求 localhost:9200/nba/_search

请求体
```json
{
    "query": {
        "match": {
            // 会进行分词匹配
            "name": "库小里"
        }
    },
    "from": 0,
    "size": 100
}
```
