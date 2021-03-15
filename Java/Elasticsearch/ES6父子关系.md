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

### 查-子查父

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

<!-- # 父子文档

## 定义

```json
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
					"type":"join",
					"relations":{
						"article":"comment"
					}
				}
			}
		}
	}
}
```

其中的"comments"字段类型定义为```join```, comment在article内定义表示article是父comment是子。

## 增

```json
POST http://localhost:9200/blog/article/1
{
    "title":"ElasticSearch6"
}
```

- 参数routing为父文档_id
- event_join_user父子关联关系，指定name为子文档名,指定父文档id
```json
POST http://localhost:9200/blog/article/4?routing=1
{
    "content":"写的真菜",
    "comments":{
    	"name":"comment",
    	"parent":1
    }
}
```

## 查-父查子

```json
GET http://localhost:9200/blog/article/_search
{
	"query":{
		"has_parent":{
			"parent_type":"article",
			"query":{
				"match":{
					"title.keyword":"ElasticSearch6"
				}
			}
		}
	}
}
```

ES只返回了comment评论结构中的数据, 而不是全部包括文章数据也返回。

## 查-子查父

```json
GET http://localhost:9200/blog/artice/_search
{
	"query":{
		"has_child":{
			"type":"comment",
			"query":{
				"match":{
					"content":"辣鸡"
				}
			}
		}
	}
}
```

ES同样也只返回了父文档的数据, 而没有子文档的数据。 -->
