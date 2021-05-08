# nested

## 定义

```json
PUT http://localhost:9200/blog
{
  "mappings":{
    "article":{
      "properties":{
        "title":{
          "type":"text",
          "analyzer":"ik_smart",
          "fields":{
            "keyword":{
              "type":"keyword",
              "ignore_above":256
            }
          }
        },
        "comments":{
          "type":"nested",
          "properties":{
            "content":{
              "type":"text",
              "analyzer":"ik_smart",
              "fields":{
                "keyword":{
                  "type":"keyword",
                  "ignore_above":256
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 增

```json
POST http://localhost:9200/blog/article/1
{
    "title":"ElasticSearch6",
    "comments":[{
        "content":"写的真菜"
    },{
        "content":"辣鸡"
    }]
}
```

## 删

```json
POST http://localhost:9200/blog/article/1/_update
{
 "script": {
    "lang": "painless",
    "source": "ctx._source.comments.removeIf(it -> it.content == '辣鸡');"
  }
}
```

## 改

```json
POST http://localhost:9200/blog/article/1/_update
{
 "script": {
   "source": "for(e in ctx._source.comments){if (e.content == '辣鸡') {e.content = 'very good';}}" 
  }
}
```

## 查-父查子

```json
GET http://localhost:9200/blog/article/_search
{
  "query":{
    "bool":{
      "must":[{
        "match":{
          "title.keyword":"ElasticSearch6"
        }
      }]
    }
  }
}
```

## 查-子查父

```json
GET http://localhost:9200/blog/article/_search
{
  "query":{
    "bool":{
      "must":[{
        "nested":{
          "path":"comments",
          "query":{
            "bool":{
              "must":[{
                "match":{
                  "comments.content":"辣鸡"
                }
              }]
            }
          }
        }
      }]
    }
  }
}
```

<!-- 

# 父子文档

-->
