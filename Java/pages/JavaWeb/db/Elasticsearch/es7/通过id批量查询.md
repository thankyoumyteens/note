# 通过id批量查询

POST请求 localhost:9200/nba/_search

请求体
```json
{
    "query": {
        "ids": {
            "values": [1, 2, 3]
        }
    },
    "from": 0,
    "size": 3
}
```
